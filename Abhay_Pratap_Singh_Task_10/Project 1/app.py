import pandas as pd
from flask import Flask, render_template, request
import pickle

with open('/Users/abhay/Desktop/Probation/Probation-Project-25/Abhay_Pratap_Singh_Task_10/Project 1/coemissions_classifier_model.pkl', 'rb') as f:
    ct, rf = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    year = 2000
    make = request.form['make']
    model = request.form['model']
    vehicle_class = request.form['vehicle_class']
    engine_size = float(request.form['engine_size'])
    cylinders = int(request.form['cylinders'])
    transmission = request.form['transmission']
    fuel = request.form['fuel']
    fuel_consumption = float(request.form['fuel_consumption'])

    input_data = [[make, model, vehicle_class, engine_size, cylinders,
                   transmission, fuel, fuel_consumption]]

    df = pd.DataFrame(input_data, columns=['make', 'model', 'vehicle_class',
                                            'engine_size', 'cylinders',
                                            'transmission', 'fuel',
                                            'fuel_consumption'])

    prediction = rf.predict(ct.transform(df))
    return render_template('index.html', result=str(prediction[0]))

if __name__ == '__main__':
    app.run(debug=True)