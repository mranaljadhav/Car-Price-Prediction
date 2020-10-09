import numpy as np
from flask import Flask, request, jsonify, render_template, url_for
import pickle

app = Flask(__name__)
model = pickle.load(open('car_pred.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    Fuel_Type_Diesel=0
    if  request.method == 'POST':
        Present_Price = float(request.form['Present_Price'])
        
        Year = int(request.form['Year'])
        Year = 2020 - Year
        
        Kms_Driven = int(request.form['Kms_Driven'])
        Kms_Driven2 = np.log(Kms_Driven)
        
        Owner=int(request.form['Owner'])
        
        Fuel_Type_Petrol = request.form['Fuel_Type_Petrol']
        if(Fuel_Type_Petrol == 'Petrol'):                                                        
            Fuel_Type_Petrol = 1
            Fuel_Type_Diesel = 0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Diesel = 1
            
        Transmission_Manual = request.form['Transmission_Manual']
        if(Transmission_Manual == 'Manual'):
            Transmission_Manual = 1
        else :
            Transmission_Manual = 0
        
        Seller_Type_Individual = request.form['Seller_Type_Individual']
        if(Seller_Type_Individual == 'Individual'):
             Seller_Type_Individual = 1
        else:
            Seller_Type_Individual = 0
        
        prediction = model.predict([[Present_Price,Kms_Driven2,Owner,Year,Fuel_Type_Diesel,Fuel_Type_Petrol,Seller_Type_Individual,Transmission_Manual]])
        output = round(prediction[0], 2)
        if output < 0:
            return render_template('index.html', prediction_text = "You can't sell the car")     
        else :
            return render_template('index.html', prediction_text='Car Price should be {} lakh'.format(output))
   
    else:
        return render_template('index.html')
    
if __name__=="__main__":
    app.run(debug=True)
