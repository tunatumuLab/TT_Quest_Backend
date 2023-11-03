import openai

# OpenAIの API Key
openai.api_key = "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"

# カテゴリ一覧の取得 (カテゴリは ver.3.5のほうが筋が良さそう)
def gen_category_list(test_name):
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "フォーマルに答えてください"},
        {"role": "user", "content": "ITパスポートで出題されるような問題のカテゴリを、カンマ区切りで出力してください。ただし、要素数は10以内でお願いします"}
    ]   
  )
  _list_category = response["choices"][0]["message"]["content"].split(',')

  return _list_category


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
