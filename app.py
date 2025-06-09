from flask import Flask, render_template, request
import joblib
import pandas as pd
from weather_API import get_combined_weather

app = Flask(__name__)

model = joblib.load("flooden_model_all.pkl")
OPENWEATHER_API_KEY = "dff0a34ec7ec59d3828240dbccc14d76"

lokasi_koordinat = {
    'jakarta_utara': (-5.85, 106.82),
    'jakarta_selatan': (-6.28, 106.82),
    'jakarta_pusat': (-6.17, 106.82)
}

lokasi_nama_map = {
    'jakarta_utara': "Jakarta Utara",
    'jakarta_selatan': "Jakarta Selatan",
    'jakarta_pusat': "Jakarta Pusat"
}

feature_names = [
    "Tn", "Tx", "Tavg", "RH_avg", "RR",
    "ss", "ff_x", "ddd_x", "ff_avg", "cat_ddd", "category_region"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    weather_data = None
    lokasi_nama = None  # default None

    if request.method == 'POST':
        lokasi = request.form.get('location', 'jakarta_pusat')
        lat, lon = lokasi_koordinat.get(lokasi, (-6.17, 106.82))
        lokasi_nama = lokasi_nama_map.get(lokasi, "Jakarta Pusat")

        try:
            weather_data = get_combined_weather(lokasi, OPENWEATHER_API_KEY, lat, lon)

            data_input = [
                weather_data['temp_min'],
                weather_data['temp_max'],
                weather_data['temp_avg'],
                weather_data['humidity'],
                weather_data['rain_1h'],
                weather_data['solar_radiation'],
                weather_data['wind_speed'],
                weather_data['wind_deg'],
                weather_data['wind_speed_nasa'],
                weather_data['wind_deg'],
                1
            ]

            input_df = pd.DataFrame([data_input], columns=feature_names)
            pred = model.predict(input_df)[0]
            result = (
                '<span class="material-icons-outlined align-middle mr-2">warning</span> POTENSI BANJIR TERDETEKSI!'
                if pred == 1
                else '<span class="material-icons-outlined align-middle mr-2">check_circle</span> TIDAK ADA POTENSI BANJIR'
            )

        except Exception as e:
            result = f"Terjadi error saat prediksi: {e}"

    return render_template("index.html", result=result, data=weather_data, lokasi_nama=lokasi_nama)

if __name__ == '__main__':
    app.run(debug=True)
