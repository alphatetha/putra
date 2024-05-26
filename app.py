from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
import os

app = Flask(__name__)

# Fungsi untuk melakukan prediksi dan perhitungan
def calculate_predictions(period, current_age):
    # Memuat data
    data1 = pd.read_csv('GI.csv')
    
    #sumbu X adalah Periode dan sumbu Y adalah Beban Transformator
    x1 = data1.iloc[:, :-1].values
    y1 = data1.iloc[:, -1].values

    # Memisahkan fitur dan target   
    x1 = data1[['Periode']]
    y1 = data1['Beban']

    # Memecah data menjadi data pelatihan dan pengujian
    x1_train, x1_test, y1_train, y1_test = train_test_split(x1, y1, test_size=0.2, random_state=0)

    # Membuat dan melatih model regresi linear
    regressor1 = LinearRegression()
    regressor1.fit(x1_train, y1_train)

    # Menampilkan nilai a dan b dari persamaan regresi linear
    a1 = regressor1.intercept_
    b1 = regressor1.coef_[0]

    # Melakukan prediksi
    prediksi1 = a1 + (b1 * period)

    # Menghitung θH1
    Tmax1 = 98  # Suhu Maksimum
    θH1 = (prediksi1 * Tmax1) / 100
    # Menghitung V1
    V1 = 2 ** ((θH1 - 98) / 6)
    # Menghitung Susut Umur1
    susut_umur1 = 24 * V1
    # Menghitung Sisa Umur1
    umur_dasar1 = 20
    sisa_umur1 = (umur_dasar1 - current_age) / susut_umur1

    return {
        "prediksi_beban": prediksi1,
        "θH": θH1,
        "V": V1,
        "susut_umur": susut_umur1,
        "sisa_umur": sisa_umur1
    }

@app.route('/')
def index():
    print("Current working directory:", os.getcwd())
    return render_template('gipatuha.html', 'gilagadar.html', 'gibdgsltn.html')

@app.route('/predict', methods=['POST'])
def predict():
    period = int(request.form['periode'])
    current_age = float(request.form['current_age'])
    results = calculate_predictions(period, current_age)

    return render_template('gipatuha.html', 'gilagadar.html','gibdgsltn.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
