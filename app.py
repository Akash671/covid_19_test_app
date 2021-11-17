import flask
import pickle
import pandas as pd

#import libraries
import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle



# Use pickle to load in the pre-trained model
with open(f'model/covid_19_test_model.pkl', 'rb') as f:
    model = pickle.load(f)


app = Flask(__name__)


#default page of our web-app
@app.route('/')
def home():
    return render_template('main.html')

#To use the predict button in our web-app
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    output=""
    int_features = []
    a= [ x for x in request.form.values()]
    #print(a)
    try:
     for i in range(1,len(a)):
       if a[i]=='male' or a[i]=='MALE' or a[i]=='Male':
           int_features.append(1)
       elif a[i]=='female' or a[i]=='FEMALE' or a[i]=='Female':
           int_features.append(0)
       elif a[i]=='yes' or a[i]=='Yes' or a[i]=='YES':
           int_features.append(1)
       elif a[i]=='no' or a[i]=='NO' or a[i]=='No':
           int_features.append(0)
       else:
          int_features.append(float(a[i]))
     #print(int_features)
     final_features = [np.array(int_features)]
     prediction = model.predict(final_features)
     #output=""
     if prediction[0]==0:
       output="Test is Negative"
     else:
       output='Test is Positive'
     #output = round(prediction[0], 2)
    
     #return render_template('index.html', prediction_text='CO2 Emission of the vehicle is :{}'.format(output))
     return render_template('main.html', prediction_text='Your Corona {}'.format(output))
    except:
       output="Test Failed!!!!"
       return render_template('main.html', prediction_text='Your Corona {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
