import streamlit as st
import pandas as pd
import spacy

# SpaCyの英語モデルをロード
nlp = spacy.load("en_core_web_sm")

# CSVファイルのURL
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

df_e = load_data(CSV_URL_E)
df_j = load_data(CSV_URL_J)
df_he = load_data(CSV_URL_HE)
df_hl = load_data(CSV_URL_HL)

required_columns_e = ["Item", "Frequency", "語彙レベル", "R2", "BS", "HWG", "NC", "NH", "OW", "SS"]
required_columns_j = ["Item", "Frequency", "語彙レベル", "BS", "HWG", "NC", "NH", "OW", "SS"]

def validate_columns(df, required_columns):
    missing = [col for col in required_columns if col not in df.columns]
    if missing:
        st.error(f"以下のカラムが欠けています: {', '.join(missing)}")
        return False
    return True

if not validate_columns(df_e, required_columns_e) or not validate_columns(df_j, required_columns_j):
    st.stop()

st.title("TeachLex Scope")
st.markdown("""
<p style="font-size:16px;">小学校から高等学校の英語の教科書の使用状況をお知らせします。</p>
""", unsafe_allow_html=True)

# 単語のlemmaを取得する関数
def get_lemma(input_word):
    try:
        doc = nlp(input_word)
        return doc[0].lemma_  # 最初の単語のlemmaを返す
    except Exception as e:
        st.error(f"Lemma取得中にエラーが発生しました: {e}")
        return ""

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 単語を検索")
    word = st.text_input("単語を入力してください", "")

with col2:
    if word:  # テキストボックスに入力があった場合のみ処理を実行
        lemma_word = get_lemma(word)  # 入力された単語をlemmaに変換
        st.write(f"入力された単語: {word} → lemma形式: {lemma_word}")

        # 小学校の教科書の使用状況
        result_e = df_e[df_e["Item"] == lemma_word]
        if not result_e.empty:
            st.subheader("小学校の教科書の使用状況")
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{result_e['Frequency'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_e['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>R2年版教科書の頻度: <b style='font-size:18px;'>{result_e['R2'].values[0]}</b></p>", unsafe_allow_html=True)

            textbooks = ["R2", "BS", "HWG", "NC", "NH", "OW", "SS"]
            states = [result_e[book].values[0] if result_e[book].values[0] != 0 else "×" for book in textbooks]
            data_e = pd.DataFrame([textbooks, states], index=["教科書名", "使用頻度"])
            st.table(data_e)
        else:
            st.warning("入力された単語は小学校のリストに含まれていません。")

        # 中学校の教科書の使用状況
        result_j = df_j[df_j["Item"] == lemma_word]
        if not result_j.empty:
            st.subheader("中学校の教科書の使用状況")
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{result_j['Frequency'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_j['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)

            textbooks = ["BS", "HWG", "NC", "NH", "OW", "SS"]
            states = [result_j[book].values[0] if result_j[book].values[0] != 0 else "×" for book in textbooks]
            data_j = pd.DataFrame([textbooks, states], index=["教科書名", "使用頻度"])
            st.table(data_j)
        else:
            st.warning("入力された単語は中学校のリストに含まれていません。")

        # 高等学校英語コミュニケーション
        result_he = df_he[df_he["単語"] == lemma_word]
        if not result_he.empty:
            st.markdown("---")
            st.subheader("高等学校英語コミュニケーションの使用状況")
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_he['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{int(result_he['ARF'].values[0])}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>使用教科書数: <b style='font-size:18px;'>{int(result_he['使用教科書数'].values[0])}</b></p>", unsafe_allow_html=True)
        else:
            st.warning("入力された単語は英語コミュニケーションのリストに含まれていません。")

        # 高等学校論理表現
        result_hl = df_hl[df_hl["単語"] == lemma_word]
        if not result_hl.empty:
            st.markdown("---")
            st.subheader("高等学校論理表現の使用状況")
            st.markdown(f"<p style='font-weight:normal;'>語彙レベル: <b style='font-size:18px;'>{result_hl['語彙レベル'].values[0]}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>頻度: <b style='font-size:18px;'>{int(result_hl['ARF'].values[0])}</b></p>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-weight:normal;'>使用教科書数: <b style='font-size:18px;'>{int(result_hl['使用教科書数'].values[0])}</b></p>", unsafe_allow_html=True)
        else:
            st.warning("入力された単語は論理表現のリストに含まれていません。")
    else:
        st.warning("ここに結果が表示されます")
