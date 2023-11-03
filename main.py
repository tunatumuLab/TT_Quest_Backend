from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要

app = FastAPI()


# リクエストbodyを定義
class User(BaseModel):
    user_id: int
    name: str

class Dungeon(BaseModel):
    name: str

class Stage(BaseModel):
    dungeon_name: str
    stage_name: str

# 使わない
class Question(BaseModel):
    question: str
    answer_index: int
    options = []
    level: int

# ダンジョン生成（実際にはダンジョン内のステージ名を生成）
@app.post("/create-stages/")
def create_stages(dungeon: Dungeon):
    # テスト用の固定値
    return {"stages": [ "確率と確率変数", "種々の確率分布", "統計的推測（推定）", "統計的推測（検定）", "データ解析・分析手法" ] }

# 問題生成
@app.post("/create-questions/")
def create_questions(stage: Stage):
    # テスト用の固定値
    return {"question": "問題文問題文問題文", "answer_index": 2, "options": [ "選択肢A", "選択肢B", "選択肢C", "選択肢D" ], "level": 3 }

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
