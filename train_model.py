import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib

# تحميل البيانات من fichier CSV
df = pd.read_csv("model.csv")

# تحويل النتائج إلى أرقام
label_encoder = LabelEncoder()
df["result_encoded"] = label_encoder.fit_transform(df["result"])

# اختيار الميزات والهدف
X = df[["home_goals_avg", "away_goals_avg"]]
y = df["result_encoded"]

# تدريب النموذج
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# حفظ النموذج والمحول
joblib.dump(model, "model.pkl")
joblib.dump(label_encoder, "label_encoder.pkl")

print("✅ تم تدريب النموذج وحفظه في model.pkl و label_encoder.pkl")