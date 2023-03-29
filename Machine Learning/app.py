import numpy as np
from flask import Flask, request, render_template
import pickle

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

scalerfile = 'scaler.sav'
scaler = pickle.load(open(scalerfile, 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''

    data = request.form
    tipe = request.form.get('tipe')
    kdm = request.form.get('kdm')
    wifi = request.form.get('wifi')
    ac = request.form.get('ac')
    kd = request.form.get('kd')
    kasur = request.form.get('kasur')

    data = {
        'putra':0,
        'putri':0,
        'ac':ac,
        'wifi':wifi,
        'kasur':kasur,
        'kdm':kdm,
        'kd':kd,
    }

    if(tipe == 'perempuan'):
        data['putri'] = 1
    elif(tipe == 'laki-laki'):
        data['putra'] = 1
    
    for i in data:
        if(data[i] == 'on'):
            data[i] = 1
        elif(data[i] == None):
            data[i] = 0

    int_features = [int(data[x]) for x in data]
    final_features = [np.array(int_features)]
    prediction = model.predict(final_features)

    prediction = scaler.inverse_transform([prediction])

    print(data)
    print(int_features)
    print(prediction)
    return render_template('index.html', prediction_text='Berdasarkan dari tipe dan fasilitas yang diinginkan maka prediksi harga yang didapat adalah : Rp. {}'.format(round(prediction[0][0])))

if __name__ == "__main__":
    app.run(debug=True) 