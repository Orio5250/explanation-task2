import streamlit as st

# クイズデータ：文法、データ構造、例外処理の純粋な意味に特化
quiz_data = [
    {
        "code": "if not word:",
        "question": "この条件式 `not word` が真（True）判定されるのは、変数 word がどのような状態のときですか？",
        "options": [
            "word に数値が入っているとき",
            "word が空文字列（\"\"）のとき",
            "word に \"None\" という文字列が入っているとき",
            "word が 10文字以上のとき"
        ],
        "answer": "word が空文字列（\"\"）のとき"
    },
    {
        "code": "response.raise_for_status()",
        "question": "このメソッドの純粋な役割は何ですか？",
        "options": [
            "Webページをブラウザで開く",
            "ステータスコードがエラー（4xx, 5xx）の場合に例外（HTTPError）を発生させる",
            "取得したデータをすべて大文字に変換する",
            "インターネットの接続速度を測定する"
        ],
        "answer": "ステータスコードがエラー（4xx, 5xx）の場合に例外（HTTPError）を発生させる"
    },
    {
        "code": "entry.get('phonetic', '不明')",
        "question": "辞書オブジェクトの `.get()` メソッドで、第2引数に '不明' と書く意味は何ですか？",
        "options": [
            "キー 'phonetic' が存在しない場合に、代わりの値として '不明' を返す",
            "'phonetic' という値を辞書から削除して '不明' に書き換える",
            "常に '不明' という値を返すように強制する",
            "'phonetic' が '不明' という文字列と一致するか判定する"
        ],
        "answer": "キー 'phonetic' が存在しない場合に、代わりの値として '不明' を返す"
    },
    {
        "code": "entry['meanings'][0]['definitions']",
        "question": "この記述から推測される、変数 entry のデータ構造の説明として正しいものはどれですか？",
        "options": [
            "entryは単なる1つの文字列である",
            "entryは辞書で、その中に 'meanings' というキーがあり、その値はリストである",
            "entryは3次元の数値配列である",
            "entryは definitions という名前の関数を呼び出している"
        ],
        "answer": "entryは辞書で、その中に 'meanings' というキーがあり、その値はリストである"
    },
    {
        "code": "except requests.exceptions.RequestException as e:",
        "question": "この `as e` という記述の役割は何ですか？",
        "options": [
            "エラーが発生しても無視して実行を続ける",
            "発生したエラー（例外）の情報を変数 e に格納して利用できるようにする",
            "e という名前の新しい関数を作成する",
            "プログラムを強制終了して Windows の Eドライブに保存する"
        ],
        "answer": "発生したエラー（例外）の情報を変数 e に格納して利用できるようにする"
    }
]

# --- Streamlit 表示制御 ---
st.set_page_config(page_title="API Code Logic Quiz", layout="centered")

st.title("🧩 Python構造・例外処理クイズ")
st.write("コードの「構文」と「データの辿り方」を正確に理解しましょう。")

if 'idx' not in st.session_state:
    st.session_state.idx = 0
    st.session_state.correct_count = 0
    st.session_state.done = False

if not st.session_state.done:
    item = quiz_data[st.session_state.idx]
    
    st.markdown(f"### 第 {st.session_state.idx + 1} 問")
    st.code(item["code"], language="python")
    
    with st.form(key=f"syntax_form_{st.session_state.idx}"):
        st.write(item["question"])
        user_answer = st.radio("選択してください:", item["options"], index=None)
        
        btn = st.form_submit_button("回答確定")
        
        if btn:
            if user_answer == item["answer"]:
                st.session_state.correct_count += 1
                st.success("Correct!")
            else:
                st.error(f"Incorrect... 正解は: {item['answer']}")
            
            if st.session_state.idx + 1 < len(quiz_data):
                st.session_state.idx += 1
                st.form_submit_button("次の問題へ")
            else:
                st.session_state.done = True
                st.form_submit_button("結果を表示")

else:
    st.header("🏁 クイズ終了")
    score = st.session_state.correct_count
    total = len(quiz_data)
    st.metric("スコア", f"{score} / {total}")
    
    # 階層構造の視覚的ヒント（復習用）
    st.write("---")
    st.write("💡 **復習ポイント：辞書とリストの階層**")
    st.write("今回のようなAPIデータ（JSON）は、以下のような構造を辿っています。")
    st.code("data[0] -> リストの1番目\n  ['meanings'] -> 辞書のキーを選択\n    [0] -> リストの1番目\n      ['definitions'] -> 辞書のキーを選択", language="text")

    if st.button("再挑戦"):
        st.session_state.idx = 0
        st.session_state.correct_count = 0
        st.session_state.done = False
        st.rerun()
