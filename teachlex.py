import streamlit as st
import pandas as pd
import spacy

# SpaCyの英語モデルをロード
nlp = spacy.load("en_core_web_sm")

# 小学校、中学校、高等学校英語コミュニケーション、高等学校論理表現のCSVファイルのURL
CSV_URL_E = "http://hirosakieigo.weblike.jp/appdvlp/txtbk/vocabdata_E.csv"
CSV_URL_J = "http://hirosakieigo.weblike.jp/appdvlp/txtbk/vocabdata_J.csv"
CSV_URL_HE = "http://hirosakieigo.weblike.jp/appdvlp/txtbk/vocabdata_HE.csv"
CSV_URL_HL = "http://hirosakieigo.weblike.jp/appdvlp/txtbk/vocabdata_HL.csv"

@st.cache_data
def load_data(url):
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"データ読み込み中にエラーが発生しました: {e}")
        return pd.DataFrame()

def validate_columns(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"以下のカラムが欠けています: {', '.join(missing)}")
        return False
    return True

df_e = load_data(CSV_URL_E)
df_j = load_data(CSV_URL_J)
df_he = load_data(CSV_URL_HE)
df_hl = load_data(CSV_URL_HL)

required_columns = ["単語", "頻度", "語彙レベル"]
if not validate_columns(df_e, required_columns) or not validate_columns(df_j, required_columns):
    st.stop()

st.title("TeachLex Scope")
st.markdown("""
<p style="font-size:16px;">小学校から高等学校の英語の教科書の使用状況をお知らせします。</p>
""", unsafe_allow_html=True)

# レイアウト設定
col1, col2 = st.columns([1, 2])

# 単語のlemmaを取得する関数
def get_lemma(input_word):
    try:
        doc = nlp(input_word)
        return doc[0].lemma_  # 最初の単語のlemmaを返す
    except Exception as e:
        st.error(f"Lemma取得中にエラーが発生しました: {e}")
        return ""

with col1:
    st.markdown("### 単語を検索")
    word = st.text_input("単語を入力してください", "")

with col2:
    if word:  # テキストボックスに入力があった場合のみ処理を実行
        lemma_word = get_lemma(word)  # 入力された単語をlemmaに変換
        st.write(f"入力された単語: {word} → lemma形式: {lemma_word}")

        # 各教科書データの確認
        def display_usage(df, title, additional_cols=None):
            result = df[df["単語"] == lemma_word]
            if not result.empty:
                st.subheader(title)
                st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{result['頻度'].values[0]}</b></p>", unsafe_allow_html=True)
                st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)
                
                if additional_cols:
                    for col in additional_cols:
                        st.markdown(f"<p style='font-weight:normal;'>{col}: <b style='font-size:18px;'>{result[col].values[0]}</b></p>", unsafe_allow_html=True)

                textbooks = result.columns[3:]  # 教科書名列
                states = ['〇' if result[book].values[0] else '×' for book in textbooks]
                data = pd.DataFrame([textbooks, states], index=["教科書名", "使用の有無"])
                st.table(data)
            else:
                st.warning(f"入力された単語は{title}のリストに含まれていません。")

        # 小学校
        display_usage(df_e, "小学校の教科書の使用状況")
        # 中学校
        display_usage(df_j, "中学校の教科書の使用状況")
        # 高等学校英語コミュニケーション
        display_usage(df_he, "高等学校英語コミュニケーション", ["ARF", "使用教科書数"])
        # 高等学校論理表現
        display_usage(df_hl, "高等学校論理表現", ["ARF", "使用教科書数"])
    else:
        st.warning("ここに結果が表示されます")
