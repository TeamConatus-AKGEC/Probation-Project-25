from flask import Flask, render_template, request
import pandas as pd
import joblib
import numpy as np
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "best_model2.joblib")
data_path = os.path.join(BASE_DIR, "AdultIncome.csv")

model = joblib.load(model_path)
df = pd.read_csv(data_path)

df.replace('?', pd.NA, inplace=True)

unique_values = {}
for col in df.columns:
    if df[col].dtype == 'object':
        clean_vals = df[col].dropna().unique().tolist()
        unique_values[col] = sorted([v for v in clean_vals if v is not pd.NA])

X = df.drop(columns=["income"])

@app.route("/")
def home():
    return render_template("index.html", unique_values=unique_values)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_data = []
        for col in X.columns:
            val = request.form[col]
            try:
                val = float(val)
            except ValueError:
                pass
            input_data.append(val)

        input_array = np.array([input_data], dtype=object)

        prediction = model.predict(input_array)[0]

        return render_template(
            "index.html",
            unique_values=unique_values,
            prediction_text=f"Predicted Income: {prediction}"
        )
    except Exception as e:
        return render_template(
            "index.html",
            unique_values=unique_values,
            prediction_text=f"Error: {e}"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
