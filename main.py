from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要
from starlette.middleware.cors import CORSMiddleware

import call_openai
import json
import asyncio
import math
import os
from concurrent.futures import ProcessPoolExecutor


app = FastAPI()

# CORSを回避するために追加
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

# リクエストbodyを定義
class User(BaseModel):
    user_id: int
    name: str

class Dungeon(BaseModel):
    name: str

class Stage(BaseModel):
    dungeon_name: str
    stage_name: str
    difficulity: int

class Question(BaseModel):
    question: str
    answer_index: int
    options = []
    level: int

# ダンジョン生成（実際にはダンジョン内のステージ名を生成）
@app.post("/create-stages/")
def create_stages(dungeon: Dungeon):
    # openaiを用いてステージ名を生成
    _list = call_openai.gen_stage_list(dungeon.name)
    
    _stages = {"stages":"dummy"} # 仮で作成
    _stages["stages"] = _list
    
    return _stages
    
#    # テスト用の固定値
#    return {"stages": [ "確率と確率変数", "種々の確率分布", "統計的推測（推定）", "統計的推測（検定）", "データ解析・分析手法" ] }

# 問題生成
@app.post("/create-questions/")
def create_questions(stage: Stage):
    # テスト用の固定値
    _questions = call_openai.gen_question_list(stage.dungeon_name, stage.stage_name)
    questions = {"questions": "dummy"}

    questions["questions"] = _questions

#    questions = []
#    questions.append({"question": "問題文1問題文1問題文1", "answer_index": 1, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 1})
#    questions.append({"question": "問題文2問題文2問題文2", "answer_index": 2, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 2})
#    questions.append({"question": "問題文3問題文3問題文3", "answer_index": 3, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 3})
    return questions

@app.post("/create-questions-para")
async def create_questions_para(stage: Stage):
    # _questions = [call_openai.gen_one_question(stage.dungeon_name, stage.stage_name, math.ceil(i/5) ) for i in range(15)]
    # _tasks = [agent.arun(q) for q in _questions]
    # await asyncio.gather(*_tasks)
    max_workers = 3
    _questions = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        #for i in range(15)
        #    executor.submit(call_openai.gen_one_question(stage.dungeon_name, stage.stage_name, math.ceil(i/5) ))
        _questions = executor.map(call_openai.gen_one_question, [stage.dungeon_name for i in range(5)], [stage.stage_name for i in range(5)], [stage.difficulity for i in range(5)])

    questions = {"questions": "dummy"}
    questions["questions"] = _questions
    return questions   
    
# シンプルなJSON Bodyの受け取り
@app.post("/user/")
# 上で定義したUserモデルのリクエストbodyをuserで受け取る
# user = {"user_id": 1, "name": "太郎"}
def create_user(user: User):
    # レスポンスbody
    return {"res": "ok", "ID": user.user_id, "名前": user.name}


# ネストされたJSON Bodyの受け取り
@app.post("/users/")
# 上で定義したUserモデルのリクエストbodyをリストに入れた形で受け取る
# users = [{"user_id": 1, "name": "太郎"},{"user_id": 2, "name": "次郎"}]
def create_users(users: List[User]):
    new_users = []
    for user in users:
        new_users.append({"res": "ok", "ID": user.user_id, "名前": user.name})
    # 整形したデータをレスポンスbodyを送信
    return new_users

@app.get("/")
def state():
    return os.cpu_count() 
