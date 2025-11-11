from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load trained KNN model
with open("adult_best_model.pkl", "rb") as f:
    model = pickle.load(f)

# Categorical columns (from your notebook)
categorical_cols = ['workclass', 'marital.status', 'occupation', 'relationship', 'race', 'sex']

# Model training feature names
model_columns = [
    'num__age', 'num__education.num', 'num__hours.per.week',
    'num__workclass_Local-gov', 'num__workclass_Never-worked',
    'num__workclass_Private', 'num__workclass_Self-emp-inc',
    'num__workclass_Self-emp-not-inc', 'num__workclass_State-gov',
    'num__workclass_Without-pay', 'num__workclass_nan',
    'num__marital.status_Married-AF-spouse',
    'num__marital.status_Married-civ-spouse',
    'num__marital.status_Married-spouse-absent',
    'num__marital.status_Never-married', 'num__marital.status_Separated',
    'num__marital.status_Widowed', 'num__occupation_Armed-Forces',
    'num__occupation_Craft-repair', 'num__occupation_Exec-managerial',
    'num__occupation_Farming-fishing', 'num__occupation_Handlers-cleaners',
    'num__occupation_Machine-op-inspct', 'num__occupation_Other-service',
    'num__occupation_Priv-house-serv', 'num__occupation_Prof-specialty',
    'num__occupation_Protective-serv', 'num__occupation_Sales',
    'num__occupation_Tech-support', 'num__occupation_Transport-moving',
    'num__occupation_nan', 'num__relationship_Not-in-family',
    'num__relationship_Other-relative', 'num__relationship_Own-child',
    'num__relationship_Unmarried', 'num__relationship_Wife',
    'num__race_Asian-Pac-Islander', 'num__race_Black',
    'num__race_Other', 'num__race_White', 'num__sex_Male'
]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.form.to_dict()
        df = pd.DataFrame([data])

        # Convert numerics
        df[['age', 'education_num', 'hours']] = df[['age', 'education_num', 'hours']].astype(float)

        # Check unrealistic inputs
        age = df.at[0, 'age']
        hours = df.at[0, 'hours']
        if age < 16 or age > 70:
            return render_template('index.html', prediction_text="Unrealistic input: Age must be 16–70.")
        if hours < 1 or hours > 80:
            return render_template('index.html', prediction_text="Unrealistic input: Hours per week must be 1–80.")

        # Encode categoricals
        df_enc = pd.get_dummies(df)
        df_enc.columns = [('num__' + c if not c.startswith('num__') else c) for c in df_enc.columns]

        # Align with training columns
        for col in model_columns:
            if col not in df_enc.columns:
                df_enc[col] = 0
        df_enc = df_enc[model_columns]

        pred = model.predict(df_enc)[0]
        result = ">50K" if pred == 1 else "<=50K"

        return render_template('index.html', prediction_text=f"Predicted Income: {result}")

    except Exception as e:
        return render_template('index.html', prediction_text=f"Error during prediction: {e}")

if __name__ == "__main__":
    app.run(debug=True)
