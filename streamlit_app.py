import streamlit as st

# ページの設定（ワイドレイアウト）
st.set_page_config(page_title="英単語検索ツール・コード解析クイズ", layout="wide")

st.title("🧩 コード解読クイズ：英単語検索ツール（強化版）")
st.write("各行のコードがPythonとして実行している内容を、右側の選択肢から選んでください。")

# --- クイズデータ（解説文 'explanation' を追加） ---
questions = [
    {
        "line": "07 行目:",
        "code": "word = input(\"...\").strip()",
        "options": ["--- 選択してください ---", "入力値の前後から空白を除去する", "入力を数値に変換する", "入力をリスト化する"],
        "answer": "入力値の前後から空白を除去する",
        "explanation": "`.strip()` は、文字列の先頭と末尾にある空白や改行を削除するメソッドです。ユーザーの不注意なスペース入力を防ぐのに役立ちます。"
    },
    {
        "line": "09 行目:",
        "code": "if not word:",
        "options": ["--- 選択してください ---", "wordが空文字列の場合に真となる", "wordに文字が含まれる場合に真となる", "wordが数値の0の場合に真となる"],
        "answer": "wordが空文字列の場合に真となる",
        "explanation": "Pythonでは空の文字列 `\"\"` は「偽 (False)」と判定されます。`if not word` とすることで、未入力の場合に処理を中断させる（真として扱う）ことができます。"
    },
    {
        "line": "22 行目:",
        "code": "response = requests.get(request_url)",
        "options": ["--- 選択してください ---", "外部サーバーへデータを要求する", "ローカルファイルを読み込む", "サーバー上のデータを削除する"],
        "answer": "外部サーバーへデータを要求する",
        "explanation": "`requests.get()` は、指定したURL（APIエンドポイントなど）に対してHTTP GETリクエストを送り、情報を取得するための関数です。"
    },
    {
        "line": "28 行目:",
        "code": "response.raise_for_status()",
        "options": ["--- 選択してください ---", "HTTPエラーが発生した際に例外を投げる", "通信を強制的に終了する", "ステータスコードを画面に表示する"],
        "answer": "HTTPエラーが発生した際に例外を投げる",
        "explanation": "通信が成功（200番台）しなかった場合、プログラムを一時停止してエラー（例外）を発生させます。これにより、壊れたデータを処理し続けるのを防ぎます。"
    },
    {
        "line": "37 行目:",
        "code": "data = response.json()",
        "options": ["--- 選択してください ---", "JSON形式の文字列をPythonの構造体に変換する", "データを暗号化する", "データをテキストファイルとして書き出す"],
        "answer": "JSON形式の文字列をPythonの構造体に変換する",
        "explanation": "APIから返ってくるのはただの「文字列」です。`.json()` を使うことで、Pythonで扱いやすい「辞書型」や「リスト型」に自動変換します。"
    },
    {
        "line": "42 行目:",
        "code": "phonetic = entry.get('phonetic', '不明')",
        "options": ["--- 選択してください ---", "キーがない場合の初期値を設定する", "キー 'phonetic' を辞書から削除する", "常に '不明' という値を代入する"],
        "answer": "キーがない場合の初期値を設定する",
        "explanation": "辞書にキーが存在しない場合、通常はエラーになりますが、`.get(キー, デフォルト値)` を使うと、キーがなくてもエラーにせずデフォルト値を返してくれます。"
    },
    {
        "line": "46 行目:",
        "code": "definitions[:3]",
        "options": ["--- 選択してください ---", "リストの最初の3要素だけを取得する", "3番目以降の要素を取得する", "3番目の要素を削除する"],
        "answer": "リストの最初の3要素だけを取得する",
        "explanation": "スライス表記 `[:n]` は、リストの先頭から `n` 個の要素を取り出します。情報量が多い場合に表示を制限する際によく使われます。"
    },
    {
        "line": "46 行目:",
        "code": "enumerate(..., 1)",
        "options": ["--- 選択してください ---", "インデックスを1から開始してカウントする", "要素を1つ飛ばしでループする", "リストの長さを1増やす"],
        "answer": "インデックスを1から開始してカウントする",
        "explanation": "`enumerate(リスト, 開始数値)` は、ループの中で「何番目か」を数えてくれます。第2引数に `1` を指定すると、カウントが 1 から始まります。"
    }
]

# --- 画面レイアウト ---
col1, col2 = st.columns([1.2, 1])

with col1:
    st.subheader("📝 ソースコード")
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
    st.subheader("🔍 説明を選択")
    
    answers = {}
    for i, q in enumerate(questions):
        st.markdown(f"**{q['line']}** `{q['code']}`")
        answers[i] = st.selectbox(
            f"Select for {i}",
            q["options"],
            key=f"q_{i}",
            label_visibility="collapsed"
        )
        st.write("") 

# --- 判定と解説 ---
st.divider()
if st.button("解答を提出する", type="primary", use_container_width=True):
    score = sum(1 for i, q in enumerate(questions) if answers[i] == q["answer"])
    
    if score == len(questions):
        st.balloons()
        st.success(f"🎊 満点です！ Pythonの基本とAPI処理を完璧に理解しています。 ({score}/{len(questions)})")
    else:
        st.warning(f"結果: {score} / {len(questions)}")
        st.subheader("💡 復習ポイント")
        
        # 間違えた問題の解説を表示
        for i, q in enumerate(questions):
            if answers[i] != q["answer"]:
                with st.expander(f"❌ {q['line']} の解説を確認する"):
                    st.markdown(f"**あなたの選択:** {answers[i]}")
                    st.markdown(f"**正解:** <span style='color:red'>{q['answer']}</span>", unsafe_allow_html=True)
                    st.info(q["explanation"])
            else:
                st.write(f"✅ {q['line']} 正解！")
