import wikipedia
import requests
import google.generativeai as genai
import time
import os
import random

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
    
categories = [
    # 人物・団体
    "歴史上の人物", "著名人", "キャラクター", "組織・団体", "家系・血族", "職業集団", 
    "政治家", "科学者", "芸術家", "思想家", "企業家", "探検家", "発明家", "指導者", 
    "活動家", "王族・貴族", "宗教指導者", "軍人", "スポーツ選手", "教育者", "医療従事者",
    "法律家", "ジャーナリスト", "エンジニア", "建築家", "デザイナー",
    
    # 文化・芸術
    "文学", "詩", "映画・ドラマ", "音楽", "音楽ジャンル", "美術", "美術運動", 
    "演劇・舞台芸術", "伝統芸能", "アニメーション", "サブカルチャー", "ポップカルチャー",
    "小説", "散文", "戯曲", "児童文学", "批評", "文学賞", "書籍", "雑誌", "マンガ", 
    "絵画", "彫刻", "写真", "陶芸", "工芸", "建築様式", "装飾芸術", "映画ジャンル", 
    "音楽理論", "楽器", "作曲", "ダンス", "バレエ", "オペラ", "ミュージカル", "コンサート",
    "フェスティバル", "博物館", "美術館", "文化遺産", "文化政策",
    
    # 科学・技術
    "物理学", "化学", "生物学", "医学", "数学", "コンピュータ科学", "ロボット工学", 
    "発明・技術", "自然現象", "宇宙科学", "生命科学", "環境科学", "材料科学",
    "力学", "熱力学", "電磁気学", "原子物理学", "素粒子物理学", "有機化学", "無機化学", 
    "生化学", "分子生物学", "遺伝学", "生態学", "進化論", "解剖学", "生理学", "病理学", 
    "薬理学", "疫学", "代数学", "幾何学", "解析学", "統計学", "確率論", "数論", 
    "プログラミング", "アルゴリズム", "人工知能", "ネットワーク", "データベース", 
    "セキュリティ", "ソフトウェア", "ハードウェア", "機械工学", "電気工学", "土木工学", 
    "建築工学", "航空工学", "宇宙工学", "農学", "気象学", "地質学", "海洋学",
    
    # 歴史・地理
    "歴史", "戦争", "国家・地域", "地理・地形", "建築", "文明", "遺跡", "歴史的事件",
    "民族・文化圏", "都市計画", "自然環境", "気候", "先史時代", "古代史", "中世史", 
    "近世史", "近代史", "現代史", "地域史", "政治史", "経済史", "社会史", "文化史", 
    "軍事史", "外交史", "植民地", "独立運動", "革命", "改革", "王朝", "帝国", "共和国", 
    "連邦", "同盟", "大陸", "半島", "島嶼", "山脈", "河川", "湖沼", "海洋", "砂漠", 
    "草原", "森林", "ジャングル", "都市", "農村", "集落", "国境", "領土", "地政学",
    
    # 社会・政治・経済
    "政治制度", "法律", "経済システム", "貨幣・通貨", "社会問題", "事件", "教育", 
    "福祉", "貿易", "市場", "産業", "労働", "民主主義", "共和制", "君主制", "独裁制", 
    "連邦制", "中央集権", "地方自治", "選挙制度", "議会", "政党", "官僚制", "司法制度", 
    "行政", "立法", "憲法", "民法", "刑法", "国際法", "人権", "市民権", "知的財産権", 
    "資本主義", "社会主義", "共産主義", "混合経済", "自由市場", "計画経済", "金融システム", 
    "銀行", "保険", "投資", "株式市場", "国際経済", "グローバリゼーション", "公教育", 
    "私教育", "高等教育", "職業訓練", "社会保障", "医療保険", "年金制度", "貧困", "格差", 
    "差別", "移民", "難民", "環境問題", "犯罪", "テロリズム", "紛争解決",
    
    # 言語・哲学・思想
    "言語", "哲学", "倫理・道徳", "思想", "コミュニケーション", "論理学", "価値観",
    "世界観", "意識", "知識論", "言語学", "文法", "音韻論", "意味論", "語用論", "方言", 
    "公用語", "少数言語", "言語政策", "翻訳", "自然言語処理", "形而上学", "認識論", 
    "存在論", "美学", "政治哲学", "社会哲学", "科学哲学", "宗教哲学", "心の哲学", 
    "言語哲学", "倫理学", "道徳理論", "応用倫理学", "生命倫理", "環境倫理", "ビジネス倫理", 
    "イデオロギー", "保守主義", "自由主義", "社会主義思想", "無政府主義", "フェミニズム", 
    "ポストモダニズム", "実存主義", "合理主義", "経験主義", "懐疑主義",
    
    # スポーツ・ゲーム
    "スポーツ", "アスリート", "eスポーツ", "ボードゲーム", "カードゲーム", "競技", 
    "チームスポーツ", "個人競技", "レジャー活動", "オリンピック", "サッカー", "野球", 
    "バスケットボール", "テニス", "ゴルフ", "水泳", "陸上競技", "マラソン", "体操", 
    "格闘技", "武道", "冬季スポーツ", "ウィンタースポーツ", "マリンスポーツ", 
    "モータースポーツ", "自転車競技", "ラケットスポーツ", "球技", "アウトドアスポーツ", 
    "エクストリームスポーツ", "スポーツイベント", "スポーツクラブ", "スポーツリーグ", 
    "トレーニング方法", "スポーツ医学", "スポーツ心理学", "ゲーム理論", "パズル", 
    "トランプゲーム", "伝統ゲーム", "ビデオゲーム", "アーケードゲーム", "ロールプレイングゲーム",
    "シミュレーションゲーム", "戦略ゲーム", "ギャンブル",
    
    # 生活・文化・娯楽
    "食文化", "飲料", "ファッション", "伝統文化", "趣味・娯楽", "旅行", "祝祭", "儀式",
    "生活様式", "衣類", "住居", "習慣", "日常生活", "料理", "食材", "調理法", "菓子", 
    "レストラン", "食事習慣", "アルコール飲料", "ソフトドリンク", "コーヒー", "茶", "服飾", 
    "アクセサリー", "美容", "化粧", "ヘアスタイル", "ブランド", "トレンド", "民族衣装", 
    "住宅様式", "インテリア", "ガーデニング", "家具", "家電", "DIY", "収集", "園芸", 
    "手芸", "工作", "写真撮影", "観光", "リゾート", "国内旅行", "海外旅行", "バックパッキング", 
    "休暇", "宿泊施設", "交通手段", "祝日", "記念日", "伝統行事", "結婚式", "葬儀", 
    "成人式", "通過儀礼", "季節行事", "パーティー", "社交", "余暇活動",
    
    # 交通・インフラ
    "交通手段", "船・航空機", "道路", "橋梁", "通信", "エネルギー", "上下水道", 
    "公共サービス", "都市インフラ", "輸送システム", "自動車", "バス", "鉄道", "地下鉄", 
    "路面電車", "タクシー", "自転車", "バイク", "歩行者", "高速道路", "幹線道路", 
    "生活道路", "トンネル", "港湾", "空港", "駅", "ターミナル", "物流", "貨物輸送", 
    "公共交通", "交通政策", "交通規則", "電話", "インターネット", "放送", "郵便", 
    "衛星通信", "モバイル通信", "発電", "送電", "配電", "再生可能エネルギー", "化石燃料", 
    "原子力", "水力", "風力", "太陽光", "上水道", "下水道", "廃棄物処理", "リサイクル", 
    "消防", "警察", "救急医療", "災害対策",
    
    # 軍事・安全保障
    "軍事", "戦術", "軍事施設", "武器", "防衛", "安全保障", "情報活動", "国際紛争", 
    "陸軍", "海軍", "空軍", "特殊部隊", "軍事組織", "軍階級", "軍事訓練", "軍事演習", 
    "軍事同盟", "軍縮", "核抑止", "平和維持活動", "対テロ作戦", "サイバー戦", "非対称戦", 
    "情報戦", "心理戦", "国防政策", "領土防衛", "国境管理", "武器開発", "戦車", "艦船", 
    "航空機", "ミサイル", "砲兵", "小火器", "爆発物", "化学兵器", "生物兵器", "核兵器", 
    "偵察", "諜報", "暗号", "対情報", "戦争法", "軍事倫理", "民間防衛",
    
    # 宗教・信仰
    "宗教", "信仰体系", "神話", "伝説", "儀礼", "聖職者", "聖地", "教義", "宗教的実践", 
    "一神教", "多神教", "無神論", "不可知論", "キリスト教", "イスラム教", "ユダヤ教", 
    "ヒンドゥー教", "仏教", "道教", "神道", "儒教", "シク教", "ゾロアスター教", "バハイ教", 
    "ジャイナ教", "新宗教運動", "民間信仰", "アニミズム", "シャーマニズム", "トーテミズム", 
    "祈り", "瞑想", "礼拝", "巡礼", "神社", "寺院", "教会", "モスク", "シナゴーグ", 
    "修道院", "司祭", "僧侶", "イマーム", "ラビ", "聖典", "宗教歴", "宗教音楽", "宗教美術", 
    "終末論", "救済", "魂", "来世", "天国", "地獄", "カルマ", "輪廻", "預言",
    
    # 自然・環境
    "生態系", "動物", "植物", "地質", "天文", "海洋", "山岳", "森林", "気象", "自然保護", 
    "哺乳類", "鳥類", "爬虫類", "両生類", "魚類", "昆虫", "無脊椎動物", "微生物", 
    "種の多様性", "絶滅危惧種", "生物地理学", "生物分類学", "植物相", "動物相", "樹木", 
    "草本", "花卉", "果実", "種子", "菌類", "コケ", "シダ", "裸子植物", "被子植物", 
    "岩石", "鉱物", "化石", "地層", "プレートテクトニクス", "火山", "地震", "侵食", 
    "堆積", "惑星", "恒星", "銀河", "宇宙", "太陽系", "月", "彗星", "小惑星", "ブラックホール", 
    "潮汐", "海流", "珊瑚礁", "河口", "湿地", "氷河", "雪", "雨", "風", "雲", "気候変動", 
    "自然災害", "環境保全", "汚染", "生物多様性", "持続可能性",
    
    # 心理・精神
    "心理学", "行動", "感情", "精神活動", "認知", "学習", "記憶", "人格", "集団心理", 
    "発達心理学", "認知心理学", "社会心理学", "臨床心理学", "異常心理学", "神経心理学", 
    "産業心理学", "教育心理学", "スポーツ心理学", "環境心理学", "知覚", "注意", "思考", 
    "言語処理", "問題解決", "意思決定", "創造性", "直感", "モチベーション", "感情調整", 
    "ストレス", "不安", "恐怖", "喜び", "悲しみ", "怒り", "驚き", "嫌悪", "自尊心", 
    "自己認識", "自己制御", "共感", "社会的影響", "対人関係", "説得", "態度変容", 
    "偏見", "ステレオタイプ", "催眠", "睡眠", "夢",
    
    # メディア・通信
    "メディア", "ジャーナリズム", "出版", "放送", "インターネット", "広告", "PR", "情報技術", 
    "新聞", "雑誌", "書籍出版", "電子出版", "テレビ", "ラジオ", "映像制作", "録音", 
    "ストリーミング", "ウェブサイト", "ソーシャルメディア", "ブログ", "ポッドキャスト", 
    "デジタルメディア", "マスメディア", "ニュース報道", "調査報道", "特集記事", "社説", 
    "コラム", "メディア倫理", "報道の自由", "検閲", "プロパガンダ", "広告キャンペーン", 
    "マーケティング", "パブリックリレーションズ", "ブランディング", "デジタルマーケティング", 
    "コンテンツ制作", "メディアリテラシー", "情報リテラシー", "情報セキュリティ", 
    "データプライバシー", "通信プロトコル", "データ転送", "情報管理",
    
    # 芸能・エンターテイメント
    "芸能人", "パフォーマンス", "ショー", "フェスティバル", "コンサート", "観光アトラクション",
    "タレント", "俳優", "声優", "歌手", "ミュージシャン", "ダンサー", "コメディアン", 
    "マジシャン", "アイドル", "モデル", "セレブリティ", "映画監督", "プロデューサー", 
    "脚本家", "劇作家", "振付師", "演出家", "芸能事務所", "タレント発掘", "オーディション", 
    "ライブパフォーマンス", "舞台公演", "トークショー", "バラエティ番組", "音楽番組", 
    "ドラマ制作", "映画祭", "音楽祭", "演劇祭", "文化祭", "カーニバル", "テーマパーク", 
    "遊園地", "動物園", "水族館", "博物館", "美術館", "史跡", "記念碑", "観光名所", 
    "リゾート施設", "ナイトライフ", "カジノ", "ショッピングモール"
]
random_category=random.choice(categories)
length=["長め","普通の長さ","短め"]
summary="」\n「".join(query)
prompt=f"あなたは優れた創作能力を持つマシンです。以下に、複数個のWikipedia記事の「要約」部分を載せますので、あなたの好きなように組み合わせたり手直ししたりして、「{random_category}」カテゴリに関連する、オリジナリティあふれる架空のWikipedia風の要約を生成してみて。ただし、アイデアは一つだけ作るのと、回答は作り出した要約部分だけにすることを絶対に守ってください。\n「{summary}」"

#Geminiモデル選択
model=genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
print(prompt+"\n")

#生成
response=model.generate_content(prompt)
print(response.text)

prompt2 = f"あなたは優れた創作能力を持つマシンです。以下に、「{random_category}」に関連するオリジナルのWikipedia記事の要約を載せるので、それをもとに世界観を広げ、{random.choice(length)}のオリジナルのWikipedia風の記事を作成してください。記事の先頭に「# タイトル」という形式でタイトルを含め、その後に本文を続けてください。回答は作り出したWikipedia記事の部分だけにすること、生成されるコンテンツが架空であることはサイトで明示するので「架空であることを示唆する表現を入れない」こと、この二つを絶対に守ってください。\n「{response.text}」"
response2=model.generate_content(prompt2)
print(response2.text)

# 既存の処理で response2 を生成した後、次のように実装
response_text = response2.text
lines = response_text.split('\n')
title = lines[0].replace('# ', '').strip()  # タイトルを抽出
content = '\n'.join(lines[1:]).strip()      # 本文を抽出

prompt3=f"以下の文章は、Wikipedia風な文章ですか？　「申し訳ありませんが、そのような内容の文章を作ることはできません」のように、AIがユーザーのプロンプトにたいして回答を拒否するようにはなっていませんか？　Wikipedia風の文章になっていると思った場合、「Y」、そうではなく、回答を拒否しているように見えたら「N」とだけ、答えてください。\n「{response2.text}」"

#response3 = model.generate_content(prompt3)
response3="skipped"
# 応答に基づいて条件分岐
if "N" in response3:
    print("記事の生成が拒否されました。ファイルは作成されません。")
else:
    timestamp = int(time.time())
    filename = f"_articles/article-{timestamp}.md"
    os.makedirs('_articles', exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"---\ntitle: \"{title}\"\n---\n\n{content}")
    print(f"記事が {filename} に保存されました")
