from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要
from starlette.middleware.cors import CORSMiddleware

import call_openai
import json


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

class Question(BaseModel):
    question: str
    answer_index: int
    options = []
    level: int

# ダンジョン生成（実際にはダンジョン内のステージ名を生成）
@app.post("/create-stages/")
def create_stages(dungeon: Dungeon):
    # openaiを用いてステージ名を生成
    _list = call_openai.gen_category_list()
    
    _stages = {"stages":"dummy"} # 仮で作成
    _stages["stages"] = _list
    
    return _stages
    
#    # テスト用の固定値
#    return {"stages": [ "確率と確率変数", "種々の確率分布", "統計的推測（推定）", "統計的推測（検定）", "データ解析・分析手法" ] }

# 問題生成
@app.post("/create-questions/")
def create_questions(stage: Stage):
    # テスト用の固定値
    questions = []
    questions.append({"question": "問題文1問題文1問題文1", "answer_index": 1, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 1})
    questions.append({"question": "問題文2問題文2問題文2", "answer_index": 2, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 2})
    questions.append({"question": "問題文3問題文3問題文3", "answer_index": 3, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 3})
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
