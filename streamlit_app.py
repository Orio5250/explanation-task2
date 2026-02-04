import streamlit as st

# ページの設定（ワイドレイアウト）
st.set_page_config(page_title="英単語検索ツール・コード解析クイズ", layout="wide")

st.title("🧩 コード解読クイズ：英単語検索ツール")
st.write("各行のコードがPythonとして実行している**最も適切な内容**を選択してください。")

# --- クイズデータ ---
# 各問題のコード片、選択肢、正解を定義
questions = [
    {
        "line": "07 行目:",
        "code": "word = input(\"...\").strip()",
        "options": [
            "--- 選択してください ---",
            "入力された文字列から空白を取り除き、変数 word に代入する。",
            "入力された単語を辞書から検索し、その結果を変数 word に入れる。",
            "入力された文字列が数値かどうかをチェックする。"
        ],
        "answer": "入力された文字列から空白を取り除き、変数 word に代入する。"
    },
    {
        "line": "22 行目:",
        "code": "response = requests.get(request_url)",
        "options": [
            "--- 選択してください ---",
            "構築したURLに対してHTTPリクエストを送り、応答を取得する。",
            "ローカルのテキストファイルから単語データを読み込む。",
            "ブラウザを起動して指定したURLのページを表示する。"
        ],
        "answer": "構築したURLに対してHTTPリクエストを送り、応答を取得する。"
    },
    {
        "line": "37 行目:",
        "code": "data = response.json()",
        "options": [
            "--- 選択してください ---",
            "APIから届いたJSON形式のデータを、Pythonのリストや辞書に変換する。",
            "取得したデータをJSON形式のファイルとして保存する。",
            "データの形式が正しいかどうかを判定してTrue/Falseを返す。"
        ],
        "answer": "APIから届いたJSON形式のデータを、Pythonのリストや辞書に変換する。"
    },
    {
        "line": "40 行目:",
        "code": "entry = data[0]",
        "options": [
            "--- 選択してください ---",
            "返ってきたリストデータの先頭要素（最初の単語エントリ）を取り出す。",
            "dataという辞書の中から '0' というキーの値を検索する。",
            "リストの中身を空（ゼロ）にする。"
        ],
        "answer": "返ってきたリストデータの先頭要素（最初の単語エントリ）を取り出す。"
    },
    {
        "line": "42 行目:",
        "code": "phonetic = entry.get('phonetic', '不明')",
        "options": [
            "--- 選択してください ---",
            "キー 'phonetic' が存在しない場合、デフォルト値として '不明' を代入する。",
            "'phonetic' という単語の意味を '不明' に書き換える。",
            "発音記号を自動的に生成して phonetic という変数に保存する。"
        ],
        "answer": "キー 'phonetic' が存在しない場合、デフォルト値として '不明' を代入する。"
    }
]

# --- 画面レイアウトの作成 ---
col1, col2 = st.columns([1.2, 1]) # 左側を少し広めに設定

# 左カラム：ソースコードの表示
with col1:
    st.subheader("ソースコード")
    code_text = """import requests
import json

def fetch_dictionary_interactive():
    print("=== 英単語検索ツール ===")
    # ユーザーから単語を入力
    word = input("検索したい英単語を入力してください: ").strip()

    if not word:
        return

    # APIのURL構築
    base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    request_url = base_url + word

    try:
        # API実行
        response = requests.get(request_url)
        
        if response.status_code == 404:
            return
            
        response.raise_for_status()

        # 2. 取得したデータを表示
        raw_json_text = response.text
        print(raw_json_text)

        # 3. JSONをデコード
        data = response.json()
        
        # データの抽出
        entry = data[0]
        word_name = entry.get('word')
        phonetic = entry.get('phonetic', '不明')
        
        # 意味をループで表示
        definitions = entry['meanings'][0]['definitions']
        for i, d in enumerate(definitions[:3], 1):
            print(f"{i}. {d['definition']}")

    except requests.exceptions.RequestException as e:
        print(e)
    """
    st.code(code_text, language="python", line_numbers=True)

# 右カラム：設問と選択肢
with col2:
    st.subheader("説明を選択")
    
    answers_state = {}
    for i, q in enumerate(questions):
        st.markdown(f"**{q['line']}** `{q['code']}`")
        answers_state[i] = st.selectbox(
            f"説明を選んでください (q_{i})",
            q["options"],
            key=f"select_{i}",
            label_visibility="collapsed"
        )
        st.write("---")

# --- 判定と結果表示 ---
if st.button("解答を提出する", type="primary", use_container_width=True):
    correct_count = 0
    total = len(questions)
    
    for i, q in enumerate(questions):
        if answers_state[i] == q["answer"]:
            correct_count += 1
            
    if correct_count == total:
        st.balloons()
        st.success(f"完璧です！全問正解 ({correct_count}/{total})")
    elif correct_count > 0:
        st.warning(f"おしい！正解数は {correct_count}/{total} です。もう一度コードを確認してみましょう。")
    else:
        st.error("まだ正解がありません。選択肢を見直してください。")
