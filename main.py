from flask import Flask, render_template, request
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

app = Flask(__name__)

def calculate_predictions(csv_file, period, current_age):
    data = pd.read_csv(csv_file)
    x = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values

    x = data[['Periode']]
    y = data['Beban']

    #shape bentuk dari data1 (ada 2 kolom dan 30 row data)
    data.shape

    #cek info tipe data
    data.info()

    #cleaning data: cek data ada yang missing value atau tidak
    data.isnull().sum()

    #cek apakah ada nilai duplikat
    data.duplicated().sum()

    #deskripsi data berdasarkan statistik
    data.describe().round(2)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
    regressor = LinearRegression()
    regressor.fit(x_train, y_train)

    a = regressor.intercept_
    b = regressor.coef_[0]
    prediksi = a + (b * period)

    Tmax = 98
    θH = (prediksi * Tmax) / 100
    V = 2 ** ((θH - 98) / 6)
    susut_umur = 24 * V
    umur_dasar = 20
    
    sisa_umur = (umur_dasar - current_age) / susut_umur

    return {
        "prediksi_beban": prediksi,
        "θH": θH,
        "V": V,
        "susut_umur": susut_umur,
        "sisa_umur": sisa_umur
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pilihan')
def pilihan():
    return render_template('pilihan.html')

@app.route('/gipatuha')
def gipatuha():
    return render_template('gipatuha.html')

@app.route('/gibdgsltn')
def gibdgsltn():
    return render_template('gibdgsltn.html')

@app.route('/gilagadar')
def gilagadar():
    return render_template('gilagadar.html')

@app.route('/predict/<gi>', methods=['POST'])
def predict(gi):
    period = int(request.form['periode'])
    current_age = float(request.form['current_age'])

    if gi == 'patuha':
        csv_file = 'BGI1.csv'
        template = 'gipatuha.html'
    elif gi == 'bdgsltn':
        csv_file = 'BGI2.csv'
        template = 'gibdgsltn.html'
    elif gi == 'lagadar':
        csv_file = 'BGI3.csv'
        template = 'gilagadar.html'
    else:
        return "GI not found", 404

    results = calculate_predictions(csv_file, period, current_age)
    return render_template(template, results=results)

if __name__ == '__main__':
    app.run(debug=True)
