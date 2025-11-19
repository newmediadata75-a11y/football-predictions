import streamlit as st
import pandas as pd

# قاموس النصوص باللغات الثلاث
translations = {
    "fr": {"title": "Prédictions Football Multilingues ⚽","prediction": "Faire une prédiction","history": "Historique des prédictions","teamA": "Équipe A","teamB": "Équipe B","predict_btn": "Prédire","result": "Résultat"},
    "ar": {"title": "توقعات كرة القدم متعددة اللغات ⚽","prediction": "قم بعمل توقع","history": "سجل التوقعات","teamA": "الفريق A","teamB": "الفريق B","predict_btn": "توقع","result": "النتيجة"},
    "en": {"title": "Multilingual Football Predictions ⚽","prediction": "Make a prediction","history": "Prediction history","teamA": "Team A","teamB": "Team B","predict_btn": "Predict","result": "Result"}
}

# اختيار اللغة من الشريط الجانبي
lang = st.sidebar.selectbox("🌐 Language / Langue / اللغة", ["fr","ar","en"])
t = translations[lang]

st.title(t["title"])

# واجهة التوقع
st.header(t["prediction"])
teamA = st.text_input(t["teamA"])
teamB = st.text_input(t["teamB"])

if st.button(t["predict_btn"]):
    if teamA and teamB:
        # نتيجة بسيطة (placeholder)
        result = f"{teamA} vs {teamB} → {teamA} wins!"
        st.success(f"{t['result']}: {result}")
        if "history" not in st.session_state:
            st.session_state["history"] = []
        st.session_state["history"].append(result)

# سجل التوقعات
st.header(t["history"])
if "history" in st.session_state and st.session_state["history"]:
    df = pd.DataFrame(st.session_state["history"], columns=[t["result"]])
    st.table(df)
else:
    st.info("No predictions yet." if lang=="en" else 
            "Pas encore de prédictions." if lang=="fr" else 
            "لا توجد توقعات بعد.")