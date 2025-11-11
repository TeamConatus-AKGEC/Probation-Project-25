from flask import Flask, render_template, request
import pickle
import numpy as np

# Initialize Flask app
app = Flask(__name__)

# Load your trained Linear Regression model
model = pickle.load(open('linear_regression_fuel_data.pkl', 'rb'))

# List all feature names your model expects
# Replace these with the exact feature names from your training dataset
feature_names = [
    'Engine_Size', 
    'Cylinders', 
    'Fuel_Consumption_City', 
    'Fuel_Consumption_Hwy', 
    'Fuel_Consumption_Comb', 
    'Fuel_Consumption_Comb_MPG'
]

def predict(input_dict):
    """
    Convert input dictionary to numpy array and predict CO2 emission
    """
    input_array = np.array([list(input_dict.values())])
    return model.predict(input_array)[0]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def make_prediction():
    try:
        # Collect input values by feature names
        input_dict = {name: float(request.form[name]) for name in feature_names}

        # Make prediction
        prediction = predict(input_dict)
        return render_template('index.html', prediction_text=f"Predicted CO2 Emission: {prediction:.2f}")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == "__main__":
    app.run(debug=True)
