import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

df = pd.read_csv("nutrition/train_data.csv")

X = df[["avg_iron", "avg_calcium", "avg_protein", "consistency"]]
y = df["risk"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

joblib.dump(model, "nutrition_risk_model.pkl")
print("ML model trained and saved")
