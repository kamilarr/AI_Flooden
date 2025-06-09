from flask import Flask, render_template, request
import joblib
import pandas as pd
from weather_API import get_combined_weather

app = Flask(__name__)

# Load model Decision Tree
model = joblib.load("flooden_model_all.pkl")

# Masukkan API Key kamu di sini (pastikan valid dan aktif)
OPENWEATHER_API_KEY = "dff0a34ec7ec59d3828240dbccc14d76"

# Pemetaan lokasi ke koordinat
lokasi_koordinat = {
    'jakarta_utara': (-5.85, 106.82),
    'jakarta_selatan': (-6.28, 106.82),
    'jakarta_pusat': (-6.17, 106.82)
}

# Daftar nama fitur sesuai model training
feature_names = [
    "Tn", "Tx", "Tavg", "RH_avg", "RR",
    "ss", "ff_x", "ddd_x", "ff_avg", "cat_ddd", "category_region"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    weather_data = None

    if request.method == 'POST':
        lokasi = request.form.get('location', 'jakarta_pusat')
        lat, lon = lokasi_koordinat.get(lokasi, (-6.17, 106.82))

        try:
            # Ambil data cuaca gabungan
            weather_data = get_combined_weather(lokasi, OPENWEATHER_API_KEY, lat, lon)

            # Buat input data sesuai urutan fitur
            data_input = [
                weather_data['temp_min'],       # Tn
                weather_data['temp_max'],       # Tx
                weather_data['temp_avg'],       # Tavg
                weather_data['humidity'],       # RH_avg
                weather_data['rain_1h'],        # RR
                weather_data['solar_radiation'],# ss
                weather_data['wind_speed'],     # ff_x
                weather_data['wind_deg'],       # ddd_x
                weather_data['wind_speed_nasa'],# ff_avg
                weather_data['wind_deg'],       # cat_ddd
                1                               # category_region (Jakarta)
            ]

            # Buat DataFrame dengan nama kolom
            input_df = pd.DataFrame([data_input], columns=feature_names)

            # Prediksi dengan model
            pred = model.predict(input_df)[0]
            result = (
                '<span class="material-icons-outlined align-middle mr-2">warning</span> POTENSI BANJIR TERDETEKSI!'
                if pred == 1
                else '<span class="material-icons-outlined align-middle mr-2">check_circle</span> TIDAK ADA POTENSI BANJIR'
            )


        except Exception as e:
            result = f"Terjadi error saat prediksi: {e}"

    return render_template("index.html", result=result, data=weather_data)

if __name__ == '__main__':
    app.run(debug=True)