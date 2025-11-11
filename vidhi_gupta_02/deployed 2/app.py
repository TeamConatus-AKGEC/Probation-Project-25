from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import joblib
import os

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "best_model2.joblib")
data_path = os.path.join(BASE_DIR, "AdultIncome.csv")
encoders_path = os.path.join(BASE_DIR, "label_encoders.joblib")

# Load model
model = joblib.load(model_path)

# Load label encoders (if saved during training)
if os.path.exists(encoders_path):
    label_encoders = joblib.load(encoders_path)
else:
    label_encoders = {}

# Load dataset for dropdowns
df = pd.read_csv(data_path)
df.replace("?", pd.NA, inplace=True)
df.dropna(inplace=True)

# Drop columns not used for training
drop_cols = ["income", "fnlwgt", "capital.gain", "capital.loss"]
X = df.drop(columns=drop_cols, errors="ignore")

# Separate categorical and numeric columns
categorical_cols = X.select_dtypes(include="object").columns
numeric_cols = X.select_dtypes(exclude="object").columns

# Unique values for dropdowns
unique_values = {
    col: sorted(df[col].dropna().unique().tolist())
    for col in categorical_cols
}

@app.route("/")
def home():
    return render_template(
        "index.html",
        unique_values=unique_values,
        numeric_cols=numeric_cols
    )

@app.route("/predict", methods=["POST"])
def predict():
    try:
        input_dict = {}
        for col in X.columns:
            val = request.form.get(col)
            if val is None or val == "":
                return render_template(
                    "index.html",
                    unique_values=unique_values,
                    numeric_cols=numeric_cols,
                    prediction_text=f"Error: Missing value for {col}"
                )
            input_dict[col] = val

        input_df = pd.DataFrame([input_dict])

        # Encode categorical columns using same LabelEncoders
        for col in categorical_cols:
            if col in label_encoders:
                le = label_encoders[col]
                if input_df[col].iloc[0] not in le.classes_:
                    # handle unseen values gracefully
                    input_df[col] = [le.classes_[0]]
                else:
                    input_df[col] = le.transform(input_df[col])

        # Convert numeric columns to float
        for col in numeric_cols:
            input_df[col] = input_df[col].astype(float)

        # Make prediction
        prediction = model.predict(input_df)[0]

        return render_template(
            "index.html",
            unique_values=unique_values,
            numeric_cols=numeric_cols,
            prediction_text=f"Predicted Income: {prediction}"
        )

    except Exception as e:
        return render_template(
            "index.html",
            unique_values=unique_values,
            numeric_cols=numeric_cols,
            prediction_text=f"Error: {e}"
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)