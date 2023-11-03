from fastapi import FastAPI
from pydantic import BaseModel  # リクエストbodyを定義するために必要
from typing import List  # ネストされたBodyを定義するために必要

app = FastAPI()


# リクエストbodyを定義
class User(BaseModel):
    user_id: int
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
def create_stages(dungeon_name: str):
    return {"message": "hoge"}

# 問題生成
@app.post("/create-questions/")
def create_questions(stage: Stage):
    return {"message": "foo"}


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
