import streamlit as st

# クイズデータ：API通信とデータ処理の純粋な挙動にフォーカス
quiz_data = [
    {
        "code": "word = input(\"...\").strip()",
        "question": "この `.strip()` メソッドの役割は何ですか？",
        "options": [
            "入力された文字列をすべて小文字に変換する",
            "文字列の前後にある空白や改行を取り除く",
            "文字列の中に含まれる数字を削除する",
            "文字列が英単語かどうかを判定する"
        ],
        "answer": "文字列の前後にある空白や改行を取り除く"
    },
    {
        "code": "request_url = base_url + word",
        "question": "Pythonにおいて、文字列同士を `+` 演算子でつなぐとどうなりますか？",
        "options": [
            "エラーが発生する",
            "2つの文字列が連結されて1つの新しい文字列になる",
            "base_url の中に word が含まれているか検索する",
            "word の長さだけ base_url を繰り返す"
        ],
        "answer": "2つの文字列が連結されて1つの新しい文字列になる"
    },
    {
        "code": "response = requests.get(request_url)",
        "question": "この `requests.get()` は具体的にどのような動作を命令していますか？",
        "options": [
            "指定したURLからデータをダウンロードして保存する",
            "指定したURLに対してHTTP GETリクエストを送信し、応答を取得する",
            "パソコン内のローカルファイルを開く",
            "Google検索を実行する"
        ],
        "answer": "指定したURLに対してHTTP GETリクエストを送信し、応答を取得する"
    },
    {
        "code": "data = response.json()",
        "question": "この行で行われている「デコード（復号化）」とはどのような処理ですか？",
        "options": [
            "パスワードを解読している",
            "JSON形式の文字列を、Pythonで扱える辞書やリストの構造に変換している",
            "英語を日本語に翻訳している",
            "画像データをテキストデータに変換している"
        ],
        "answer": "JSON形式の文字列を、Pythonで扱える辞書やリストの構造に変換している"
    },
    {
        "code": "entry = data[0]",
        "question": "変数 `data` がリスト形式である場合、`data[0]` は何を指しますか？",
        "options": [
            "リストの最後の要素",
            "リストの最初の要素",
            "リストに含まれる要素の合計数",
            "0という名前のキーを持つデータ"
        ],
        "answer": "リストの最初の要素"
    },
    {
        "code": "for i, d in enumerate(definitions[:3], 1):",
        "question": "この `enumerate(..., 1)` の役割は何ですか？",
        "options": [
            "要素をアルファベット順に並び替える",
            "1から始まるインデックス（番号）を各要素に付与する",
            "3つの要素をランダムに抽出する",
            "データの型を数値に変換する"
        ],
        "answer": "1から始まるインデックス（番号）を各要素に付与する"
    }
]

# --- Streamlit UI 構築 ---
st.set_page_config(page_title="Web API Code Quiz", layout="centered")

st.title("🌐 Web APIコード解読クイズ")
st.write("英単語検索ツールのコードが「コンピュータに何をさせているか」を解き明かしましょう。")

# セッション状態の初期化
if 'step' not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.show_result = False

if not st.session_state.show_result:
    # 現在の問題を表示
    q = quiz_data[st.session_state.step]
    
    st.markdown(f"### Question {st.session_state.step + 1}")
    st.info("ターゲット・コード:")
    st.code(q["code"], language="python")
    
    with st.form(key=f"api_quiz_{st.session_state.step}"):
        st.write(q["question"])
        choice = st.radio("選択肢:", q["options"], index=None)
        
        submitted = st.form_submit_button("回答をチェック")
        
        if submitted:
            if choice is None:
                st.warning("選択肢を選んでください。")
            elif choice == q["answer"]:
                st.session_state.score += 1
                st.success("正解です！正確に挙動を把握していますね。")
            else:
                st.error(f"不正解です。正解は: {q['answer']}")
            
            # 進捗管理
            if st.session_state.step + 1 < len(quiz_data):
                st.session_state.step += 1
                st.form_submit_button("次の問題へ")
            else:
                st.session_state.show_result = True
                st.form_submit_button("最終スコアを見る")

else:
    # 終了画面
    st.balloons()
    st.header("Quiz Complete!")
    st.metric("正解数", f"{st.session_state.score} / {len(quiz_data)}")
    
    # ランク表示
    if st.session_state.score == len(quiz_data):
        st.write("🏆 **パーフェクト！** Pythonのデータ処理の基本が完璧に身についています。")
    elif st.session_state.score >= len(quiz_data) // 2:
        st.write("👍 **ナイス！** API連携の流れをよく理解できています。")
    else:
        st.write("📚 **復習しましょう：** `requests` ライブラリやリストのインデックス操作をもう一度確認してみてください。")

    if st.button("もう一度挑戦する"):
        st.session_state.step = 0
        st.session_state.score = 0
        st.session_state.show_result = False
        st.rerun()
