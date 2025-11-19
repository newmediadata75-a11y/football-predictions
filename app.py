import streamlit as st
import pandas as pd
import joblib

# تحميل النموذج والمحول
model = joblib.load("model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# اختيار اللغة
lang = st.sidebar.selectbox("🌐 Choisissez la langue / اختر اللغة / Choose language", ["Français", "العربية", "English"])

# نصوص حسب اللغة
texts = {
    "Français": {
        "title": "⚽ Prédire les résultats des matchs de football",
        "header": "📋 Entrez les données du match",
        "home_team": "Équipe à domicile",
        "away_team": "Équipe à l'extérieur",
        "home_avg": "Moyenne de buts de l'équipe à domicile",
        "away_avg": "Moyenne de buts de l'équipe à l'extérieur",
        "button": "🔮 Prédire le résultat",
        "result": "✅ Résultat prédit :",
        "history": "📜 Voir l'historique des prédictions"
    },
    "العربية": {
        "title": "⚽ توقع نتائج مباريات كرة القدم",
        "header": "📋 أدخل بيانات المباراة",
        "home_team": "الفريق المضيف",
        "away_team": "الفريق الضيف",
        "home_avg": "متوسط أهداف الفريق المضيف",
        "away_avg": "متوسط أهداف الفريق الضيف",
        "button": "🔮 توقع النتيجة",
        "result": "✅ التوقع:",
        "history": "📜 عرض سجل التوقعات"
    },
    "English": {
        "title": "⚽ Predict Football Match Results",
        "header": "📋 Enter Match Data",
        "home_team": "Home Team",
        "away_team": "Away Team",
        "home_avg": "Average Goals - Home Team",
        "away_avg": "Average Goals - Away Team",
        "button": "🔮 Predict Result",
        "result": "✅ Predicted Result:",
        "history": "📜 View Prediction History"
    }
}

# تحميل النصوص حسب اللغة
t = texts[lang]

# واجهة المستخدم
st.title(t["title"])
st.sidebar.header(t["header"])

home_team = st.sidebar.text_input(t["home_team"])
away_team = st.sidebar.text_input(t["away_team"])
home_goals_avg = st.sidebar.slider(t["home_avg"], 0.0, 5.0, 2.0)
away_goals_avg = st.sidebar.slider(t["away_avg"], 0.0, 5.0, 2.0)

if st.sidebar.button(t["button"]):
    input_df = pd.DataFrame({
        "home_goals_avg": [home_goals_avg],
        "away_goals_avg": [away_goals_avg]
    })

    prediction_encoded = model.predict(input_df)[0]
    prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]

    st.success(f"{t['result']} {prediction_label}")

    # حفظ التوقع في fichier historique.csv
    historique = pd.DataFrame({
        "Date": [pd.Timestamp.now()],
        "Langue": [lang],
        "Équipe à domicile": [home_team],
        "Équipe à l'extérieur": [away_team],
        "Moy. buts domicile": [home_goals_avg],
        "Moy. buts extérieur": [away_goals_avg],
        "Résultat prédit": [prediction_label]
    })

    try:
        historique.to_csv("historique.csv", mode="a", header=not pd.io.common.file_exists("historique.csv"), index=False)
    except Exception as e:
        st.warning(f"⚠️ Impossible d'enregistrer l'historique : {e}")

# عرض سجل التوقعات داخل التطبيق
with st.expander(t["history"]):
    try:
        historique_df = pd.read_csv("historique.csv")
        st.dataframe(historique_df)
    except FileNotFoundError:
        st.info("ℹ️ Aucun historique trouvé / لا يوجد سجل بعد / No history found yet.")