import wikipedia
import requests
import google.generativeai as genai
import time
import os

#Geminiと接続
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

wikipedia.set_lang("jp")

ses=requests.Session()
URL="https://ja.wikipedia.org/w/api.php"
PARAMS = {
    "action": "query",
    "format": "json",
    "list": "random",
    "rnlimit": "5",
    "rnnamespace": "0"
}
R=ses.get(url=URL,params=PARAMS)
DATA=R.json()
RANDOMS=DATA["query"]["random"]
query=[]


# 5つの記事を順番に処理
for article in RANDOMS:
    random_title = article["title"]
    
    # 記事本体を取得するためのパラメータの設定
    ARTICLE_PARAMS = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "exsectionformat": "plain",
        "titles": random_title
    }

    # 記事情報を取得
    ARTICLE_R = ses.get(url=URL, params=ARTICLE_PARAMS)
    ARTICLE_DATA = ARTICLE_R.json()
    pages = ARTICLE_DATA["query"]["pages"]
    page_id = next(iter(pages))
    query.append(pages[page_id]["extract"])
    

summary="」\n「".join(query)
prompt=f"あなたは優れた創作能力を持つマシンです。以下に、複数個のWikipedia記事の「要約」部分を載せますので、あなたの好きなように組み合わせたり手直ししたりして、オリジナリティあふれる架空のWikipedia風の要約を生成してみて。ただし、アイデアは一つだけ作るのと、回答は作り出した要約部分だけにすることを絶対に守ってください。\n「{summary}」"

#Geminiモデル選択
model=genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
print(prompt+"\n")

#生成
response=model.generate_content(prompt)
print(response.text)

prompt2 = f"あなたは優れた創作能力を持つマシンです。以下に、オリジナルのWikipedia記事の要約を載せるので、それをもとに世界観を広げ、オリジナルのWikipedia風の記事を作成してください。記事の先頭に「# タイトル」という形式でタイトルを含め、その後に本文を続けてください。回答は作り出したWikipedia記事の部分だけにすること、生成されるコンテンツが架空であることはサイトで明示するので「架空であることを示唆する表現を入れない」こと、この二つを絶対に守ってください。\n「{response.text}」"
response2=model.generate_content(prompt2)
print(response2.text)

# 既存の処理で response2 を生成した後、次のように実装
response_text = response2.text
lines = response_text.split('\n')
title = lines[0].replace('# ', '').strip()  # タイトルを抽出
content = '\n'.join(lines[1:]).strip()      # 本文を抽出

prompt3=f"以下の文章は、Wikipedia風な文章ですか？　「申し訳ありませんが、そのような内容の文章を作ることはできません」のように、AIがユーザーのプロンプトにたいして回答を拒否するようにはなっていませんか？　Wikipedia風の文章になっていると思った場合、「Y」、そうではなく、回答を拒否しているように見えたら「N」とだけ、答えてください。\n「{response2.text}」"

response3 = model.generate_content(prompt3)

# 応答に基づいて条件分岐
if "N" in response3.text:
    print("記事の生成が拒否されました。ファイルは作成されません。")
else:
    timestamp = int(time.time())
    filename = f"_articles/article-{timestamp}.md"
    os.makedirs('_articles', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: \"{title}\"\n---\n\n{content}")
    print(f"記事が {filename} に保存されました")