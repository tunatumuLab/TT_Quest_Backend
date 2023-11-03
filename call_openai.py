import openai
import os

# OpenAIの API Key
openai.api_key = os.getenv('OPENAI_KEY')


import json

def extract_longest_json_string(s: str) -> str:
    json_strings = []
    current_json_string = ""
    in_json = False
    for i in range(len(s)):
        if s[i] == "{" and not in_json:
            in_json = True
            current_json_string += s[i]
        elif s[i] == "}" and in_json:
            current_json_string += s[i]
            json_strings.append(current_json_string)
            current_json_string = ""
            in_json = False
        elif in_json:
            current_json_string += s[i]
    if len(json_strings) == 0:
        return ""
    longest_json_string = max(json_strings, key=len)
    return longest_json_string


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


# 複数の、問題・解答の組を生成（入力： カテゴリ名）
def gen_question_list(dungeon_name, stage_name):
  _messages=[
    {"role":"system", "content":'''The output should be a markdown code snippet formatted in the following schema; only values must be Japanese:
    # Please do not include anything other than JSON in your answer.

    \`\`\`json
    [
      {
         question: string,
         choices: array of string,   // four candidates of the answer.
         answer: int,   // index of the choices (start with zero)
         difficulity: string   // high, mid, low
      },
      {
         question: string,
         choices: array of string,   // four candidates of the answer.
         answer: int,   // index of the choices (start with zero)
         difficulity: string   // high, mid, low
      }
    ]
    \`\`\`
    '''},
    {"role": "user", "content": "dummy"}
  ]
  # 代入
  txt = "{0}の試験範囲のうち、{1}の理解度を問う問題を3段階の難易度で分類し、それぞれの難易度における「question, choices, answer」の組を5つずつ出力してください".format(dungeon_name,stage_name)
  _messages[1]["content"] = txt
  
  response = openai.ChatCompletion.create(
    model="gpt-4",
#    model="gpt-3.5-turbo",
    messages=_messages
  )
  
  _list_question = response["choices"][0]["message"]["content"]
  
  return _list_question


# 1組の、「問題・解答」の組を生成
def gen_one_question(dungeon_name, stage_name, difficulity):
  print("Start : ", difficulity)
  difficulity_str = ""
  if difficulity == 0:
    difficulity_str = "簡単な"
  elif difficulity == 1:
    difficulity_str = "平均的な難易度の"
  else:
    difficulity_str = "難しい"
  response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role":"system", "content":'''The output should be a markdown code snippet formatted in the following schema; only values must be Japanese:
      # Please do not include anything other than JSON in your answer.

      \`\`\`json
      {
         question: string,
         choices: array of string, This item should output four choices.  // candidates of the answer.
         answer: int,   // index of the choices (start with zero)
         difficulity: string   // high, mid, low
      }
      \`\`\`
      '''},
      {"role": "user", "content": "%sの出題範囲のうち、%sの問題で、%s問題を各項目が50文字以下で出力してください"%(dungeon_name, stage_name, difficulity_str)}
    ],
    temperature=0.9  # to be adjusted
  )
  _list_question = json.loads(extract_longest_json_string(response["choices"][0]["message"]["content"]))
  print("Finish : ", difficulity)
  
  return _list_question



###
# End of This File
###
