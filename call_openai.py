import openai
import os

# OpenAIの API Key
openai.api_key = os.getenv('OPENAI_KEY')

# カテゴリ一覧の取得 (カテゴリは ver.3.5のほうが筋が良さそう)
def gen_stage_list(dungeon_name):
  # プロンプトの ひな形（ダンジョン名を結合する）
  _prompt=[
      {"role": "system", "content": "フォーマルに答えてください"},
      {"role": "user", "content": "dummy"}
  ]
  _prompt[1]["content"] = dungeon_name + "で出題されるような問題のカテゴリを、カンマ区切りで出力してください。ただし、要素数は10以内でお願いします"

  # GPTからの回答を取得する
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=_prompt
  )
  _list_stage = response["choices"][0]["message"]["content"].split(',')

  return _list_stage


# 問題・解答の組を生成（入力： カテゴリ名）
def gen_question_list(category_name):
  response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "フォーマルに答えてください"},
        {"role": "user", "content": "ITパスポートで出題されるような問題を３段階の難易度で分類し、それぞれの難易度における例題と４択の回答案、そして正解を組みとして、２つずつ出力してください"}
    ]   
  )
  _list_category = response["choices"][0]["message"]["content"].split(',')
  
  return _list_question


###
# End of This File
###
