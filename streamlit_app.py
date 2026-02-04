import streamlit as st

# ページの設定（ワイドレイアウト）
st.set_page_config(page_title="英単語検索ツール・コード解析クイズ", layout="wide")

st.title("🧩 コード解読クイズ：英単語検索ツール（強化版）")
st.write("各行のコードがPythonとして実行している内容を、右側の選択肢から選んでください。")

# --- クイズデータ（全8問） ---
questions = [
    {
        "line": "07 行目:",
        "code": "word = input(\"...\").strip()",
        "options": ["--- 選択してください ---", "入力値の前後から空白を除去する", "入力を数値に変換する", "入力をリスト化する"],
        "answer": "入力値の前後から空白を除去する"
    },
    {
        "line": "09 行目:",
        "code": "if not word:",
        "options": ["--- 選択してください ---", "wordが空文字列の場合に真となる", "wordに文字が含まれる場合に真となる", "wordが数値の0の場合に真となる"],
        "answer": "wordが空文字列の場合に真となる"
    },
    {
        "line": "22 行目:",
        "code": "response = requests.get(request_url)",
        "options": ["--- 選択してください ---", "外部サーバーへデータを要求する", "ローカルファイルを読み込む", "サーバー上のデータを削除する"],
        "answer": "外部サーバーへデータを要求する"
    },
    {
        "line": "28 行目:",
        "code": "response.raise_for_status()",
        "options": ["--- 選択してください ---", "HTTPエラーが発生した際に例外を投げる", "通信を強制的に終了する", "ステータスコードを画面に表示する"],
        "answer": "HTTPエラーが発生した際に例外を投げる"
    },
    {
        "line": "37 行目:",
        "code": "data = response.json()",
        "options": ["--- 選択してください ---", "JSON形式の文字列をPythonの構造体に変換する", "データを暗号化する", "データをテキストファイルとして書き出す"],
        "answer": "JSON形式の文字列をPythonの構造体に変換する"
    },
    {
        "line": "42 行目:",
        "code": "phonetic = entry.get('phonetic', '不明')",
        "options": ["--- 選択してください ---", "キーがない場合の初期値を設定する", "キー 'phonetic' を辞書から削除する", "常に '不明' という値を代入する"],
        "answer": "キーがない場合の初期値を設定する"
    },
    {
        "line": "46 行目:",
        "code": "definitions[:3]",
        "options": ["--- 選択してください ---", "リストの最初の3要素だけを取得する", "3番目以降の要素を取得する", "3番目の要素を削除する"],
        "answer": "リストの最初の3要素だけを取得する"
    },
    {
        "line": "46 行目:",
        "code": "enumerate(..., 1)",
        "options": ["--- 選択してください ---", "インデックスを1から開始してカウントする", "要素を1つ飛ばしでループする", "リストの長さを1増やす"],
        "answer": "インデックスを1から開始してカウントする"
    }
]

# --- 画面レイアウト ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("ソースコード")
    code_text = """import requests
import json

def fetch_dictionary_interactive():
    print("=== 英単語検索ツール ===")
    # 07行目: ユーザーから単語を入力
    word = input("検索したい英単語を入力してください: ").strip()

    if not word:
        return

    # APIのURL構築
    base_url = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    request_url = base_url + word

    try:
        # 22行目: API実行
        response = requests.get(request_url)
        
        if response.status_code == 404:
            return
            
        # 28行目: エラーチェック
        response.raise_for_status()

        # 取得したデータを表示
        raw_json_text = response.text
        print(raw_json_text)

        # 37行目: JSONをデコード
        data = response.json()
        
        # データの抽出
        entry = data[0]
        word_name = entry.get('word')
        # 42行目: 安全なデータ取得
        phonetic = entry.get('phonetic', '不明')
        
        # 46行目: 意味をループで表示
        definitions = entry['meanings'][0]['definitions']
        for i, d in enumerate(definitions[:3], 1):
            print(f"{i}. {d['definition']}")

    except requests.exceptions.RequestException as e:
        print(e)
    """
    st.code(code_text, language="python", line_numbers=True)

with col2:
    st.subheader("説明を選択")
    
    answers = {}
    for i, q in enumerate(questions):
        st.markdown(f"**{q['line']}** `{q['code']}`")
        answers[i] = st.selectbox(
            f"Select for {i}",
            q["options"],
            key=f"q_{i}",
            label_visibility="collapsed"
        )
        st.write("") # スペース

# --- 判定 ---
st.divider()
if st.button("解答を提出する", type="primary", use_container_width=True):
    score = sum(1 for i, q in enumerate(questions) if answers[i] == q["answer"])
    
    if score == len(questions):
        st.balloons()
        st.success(f"満点です！ Pythonの基本とAPI処理を完璧に理解しています。 ({score}/{len(questions)})")
    else:
        st.warning(f"完了！ 正解数: {score} / {len(questions)}")
        st.write("間違えた箇所を見直してみましょう。特にスライスやenumerate、辞書のgetメソッドは実務でも重要です。")
