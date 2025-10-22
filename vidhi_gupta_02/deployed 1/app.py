from flask import Flask, render_template, request
import pandas as pd
from joblib import load

app = Flask(__name__)

model = load(r"C:\Users\ASUS\OneDrive\Desktop\Probation-Project-25\vidhi_gupta_02\deployed 1\best_model.joblib")
df = pd.read_csv(r"C:\Users\ASUS\OneDrive\Desktop\Probation-Project-25\vidhi_gupta_02\deployed 1\fuel consumption.csv")

categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
numeric_cols = df.select_dtypes(exclude=['object']).drop(columns=['COEMISSIONS']).columns.tolist()

unique_values = {col: sorted(df[col].dropna().unique()) for col in categorical_cols}

@app.route('/')
def home():
    return render_template('index.html', unique_values=unique_values, numeric_cols=numeric_cols)

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form.to_dict()
    input_df = pd.DataFrame([form_data])

    for col in numeric_cols:
        if col in input_df.columns:
            input_df[col] = input_df[col].astype(float)

    prediction = model.predict(input_df)[0]
    prediction = round(prediction, 2)

    return render_template(
        'index.html',
        prediction_text=f"Predicted CO Emission: {prediction}",
        unique_values=unique_values,
        numeric_cols=numeric_cols
    )

if __name__ == "__main__":
    app.run(debug=True)