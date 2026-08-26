import pandas as pd
from flask import Flask, render_template, request
import pickle

with open('/Users/abhay/Desktop/Probation/Probation-Project-25/Abhay_Pratap_Singh_Task_10/income_classifier_model.pkl', 'rb') as f:
    ct, model = pickle.load(f)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    age = request.form.get('age')
    workclass = request.form.get('workclass')
    fnlwgt = request.form.get('fnlwgt')
    education_num = request.form.get('education_num')
    marital_status = request.form.get('marital_status')
    occupation = request.form.get('occupation')
    relationship = request.form.get('relationship')
    race = request.form.get('race')
    sex = request.form.get('sex')
    capital_gain = request.form.get('capital_gain')
    capital_loss = request.form.get('capital_loss')
    hours_per_week = request.form.get('hours_per_week')
    native_country = request.form.get('native')

    input_data = [[age, workclass, fnlwgt, education_num, marital_status,
       occupation, relationship, race, sex, capital_gain,
       capital_loss, hours_per_week, native_country]]

    df = pd.DataFrame(input_data, columns=[
        'age', 'workclass', 'fnlwgt', 'education_num', 'marital_status',
        'occupation', 'relationship', 'race', 'sex', 'capital_gain',
        'capital_loss', 'hours_per_week', 'native_country'])

    prediction = model.predict(ct.transform(df))
    return render_template('index.html', result=str(prediction[0]))

if __name__ == '__main__':
    app.run(debug=True)