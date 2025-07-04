from flask import render_template, request
from app import app
import joblib
import pandas as pd
import datetime
from app.weather_API import get_combined_weather

# Load model penting
model = joblib.load("app/Model/flooden_model_important.pkl")  # path relatif disesuaikan
api_keys = {
    'openweather': 'dff0a34ec7ec59d3828240dbccc14d76',
    'visualcrossing': 'C98DPJABNAH73FHJAWDEEZSGR'
}

# Koordinat lokasi
lokasi_koordinat = {
    'jakarta_utara': (-5.85, 106.82),
    'jakarta_selatan': (-6.28, 106.82),
    'jakarta_pusat': (-6.17, 106.82),
    'jakarta_timur': (-6.225, 106.900),
    'jakarta_barat': (-6.175, 106.750)
}

lokasi_nama_map = {
    'jakarta_utara': "Jakarta Utara",
    'jakarta_selatan': "Jakarta Selatan",
    'jakarta_pusat': "Jakarta Pusat",
    'jakarta_timur': "Jakarta Timur",
    'jakarta_barat': "Jakarta Barat"
}

important_features = ["RR", "RH_avg", "Tavg"]
@app.route('/')
def home():
    return render_template("index.html")  # halaman deskripsi awal

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    result = None
    weather_data = None
    lokasi_nama = None
    tanggal_terpilih = datetime.date.today().strftime('%d %B %Y')

    if request.method == 'POST':
        lokasi = request.form.get('location', 'jakarta_pusat')
        tanggal_input = request.form.get('tanggal')

        try:
            tanggal = datetime.datetime.strptime(tanggal_input, '%Y-%m-%d').date()
            tanggal_terpilih = tanggal.strftime('%d %B %Y')
        except Exception:
            tanggal = datetime.date.today()

        lat, lon = lokasi_koordinat.get(lokasi, (-6.17, 106.82))
        lokasi_nama = lokasi_nama_map.get(lokasi, "Jakarta Pusat")

        try:
            weather_data = get_combined_weather(lokasi, api_keys, lat, lon, tanggal=tanggal.isoformat())

            data_input = [
                round(weather_data['rain_daily'], 2),
                round(weather_data['humidity'], 2),
                round(weather_data['temp_avg'], 2),
            ]

            input_df = pd.DataFrame([data_input], columns=important_features)
            pred = model.predict(input_df)[0]

            if weather_data.get("data_valid", False):
                if pred == 1:
                    result = (
                        '<span class="material-icons-outlined align-middle mr-2">warning</span>'
                        ' POTENSI BANJIR TERDETEKSI!'
                    )
                else:
                    result = (
                        '<span class="material-icons-outlined align-middle mr-2">check_circle</span>'
                        ' TIDAK ADA POTENSI BANJIR'
                    )
            else:
                result = (
                    '<span class="material-icons-outlined align-middle mr-2">error</span>'
                    ' Data cuaca tidak valid, prediksi mungkin tidak akurat.'
                )

        except Exception as e:
            result = f"❌ Terjadi error saat prediksi: {e}"

    return render_template(
        "predict.html",
        result=result,
        data=weather_data,
        lokasi_nama=lokasi_nama,
        tanggal_terpilih=tanggal_terpilih
    )
