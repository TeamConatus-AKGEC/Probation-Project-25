from flask import Flask, render_template, request
import pickle, json, os
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load artifacts saved from the notebook export
with open('numeric_cols.pkl', 'rb') as f:
    numeric_cols = pickle.load(f)  # training-time numeric column names [ENGINE SIZE, CYLINDERS, FUEL CONSUMPTION, ...] [file:63]

with open('categorical_cols.pkl', 'rb') as f:
    categorical_cols = pickle.load(f)  # ['MAKE','MODEL','VEHICLE CLASS','TRANSMISSION','FUEL'] [file:63]

with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)  # trained OneHotEncoder (use handle_unknown='ignore' when fitting for robustness) [web:42]

with open('final_feature_names.pkl', 'rb') as f:
    final_feature_names = pickle.load(f)  # exact model input schema/ordering [file:63]

with open('linear_regression_fuel_data.pkl', 'rb') as f:
    model = pickle.load(f)  # trained regression model for CO2 emissions [file:63]

# Build dropdown choices from the fitted encoder if a categories map file is not present
if os.path.exists('categories_map.json'):
    with open('categories_map.json', 'r') as f:
        categories_map = json.load(f)  # persisted choices per categorical column [web:42]
else:
    categories_map = {
        col: sorted(list(cats))
        for col, cats in zip(categorical_cols, encoder.categories_)
    }  # derive choices from encoder to avoid unseen values at inference [web:42]

def _to_float(x, default=None):
    try:
        return float(x)
    except Exception:
        return default  # simple safe casting for numeric fields [file:63]

@app.route('/', methods=['GET'])
def home():
    return render_template(
        'index.html',
        categories=categories_map,
        prediction=None,
        error=None,
        input_data=None
    )  # pass choices to template to render dropdowns for all categoricals [web:42]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        form = request.form

        # 1) Read required numeric inputs
        engine_size = _to_float(form.get('ENGINE SIZE'))
        cylinders = _to_float(form.get('CYLINDERS'))
        fuel_cons = _to_float(form.get('FUEL CONSUMPTION'))

        if engine_size is None or cylinders is None or fuel_cons is None:
            raise ValueError('Please enter valid numbers for Engine Size, Cylinders, and Fuel Consumption.')  # friendly validation [file:63]

        # 2) Compute engineered features internally (not exposed to users)
        # ENGINE_CYLINDER_RATIO = ENGINE SIZE / CYLINDERS; POWER_INDICATOR = ENGINE SIZE * CYLINDERS
        eng_cyl_ratio = (engine_size / cylinders) if cylinders not in (None, 0) else 0.0  # guard division by zero [file:63]
        power_indicator = engine_size * cylinders  # multiplicative proxy feature [file:63]

        # 3) Gather categorical inputs (dropdowns guarantee known values)
        cat_row = {
            'MAKE': form.get('MAKE') or '',
            'MODEL': form.get('MODEL') or '',
            'VEHICLE CLASS': form.get('VEHICLE CLASS') or '',
            'TRANSMISSION': form.get('TRANSMISSION') or '',
            'FUEL': form.get('FUEL') or ''
        }  # categorical columns as in training [file:63]
        cat_df = pd.DataFrame([cat_row])

        # 4) Encode categoricals using the fitted encoder
        enc = encoder.transform(cat_df)  # robust if encoder was trained with handle_unknown='ignore' [web:42]
        enc_df = pd.DataFrame(enc, columns=encoder.get_feature_names_out(categorical_cols))  # stable OHE names [web:47]

        # 5) Assemble numeric features (include engineered features; they will be kept or dropped by schema alignment)
        num_row = {
            'ENGINE SIZE': engine_size,
            'CYLINDERS': cylinders,
            'FUEL CONSUMPTION': fuel_cons,
            'ENGINE_CYLINDER_RATIO': eng_cyl_ratio,
            'POWER_INDICATOR': power_indicator
        }  # includes engineered features while keeping the core numeric set from training [file:63]
        num_df = pd.DataFrame([num_row])

        # 6) Combine and align to training schema exactly
        X = pd.concat([num_df.reset_index(drop=True), enc_df.reset_index(drop=True)], axis=1)  # combine blocks [file:63]
        for col in final_feature_names:
            if col not in X.columns:
                X[col] = 0.0  # add any missing columns required by the model schema [file:63]
        X = X[final_feature_names]  # enforce exact order and column set for inference [file:63]

        # 7) Predict
        y = model.predict(X)[0]  # returns CO2 g/km estimate [file:63]

        return render_template(
            'index.html',
            categories=categories_map,
            prediction=round(float(y), 2),
            error=None,
            input_data=form
        )  # show formatted prediction to user [file:63]
    except Exception as e:
        return render_template(
            'index.html',
            categories=categories_map,
            prediction=None,
            error=str(e),
            input_data=request.form
        )  # display friendly error and keep the inputs on screen [file:63]

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)  # production servers (e.g., gunicorn) will call app:app entrypoint [file:63]
