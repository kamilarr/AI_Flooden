from flask import Flask, render_template, request
import joblib
import pandas as pd
from weather_API import get_combined_weather
import datetime

app = Flask(__name__)

# Load model penting
model = joblib.load("flooden_model_important.pkl")
api_keys = {
    'openweather': 'dff0a34ec7ec59d3828240dbccc14d76',
    'visualcrossing': 'XYCM5KGLMGRWNETW94ADVFF65'
}

# Koordinat lokasi
lokasi_koordinat = {
    'jakarta_utara': (-5.85, 106.82),
    'jakarta_selatan': (-6.28, 106.82),
    'jakarta_pusat': (-6.17, 106.82)
}

# Nama lokasi untuk ditampilkan
lokasi_nama_map = {
    'jakarta_utara': "Jakarta Utara",
    'jakarta_selatan': "Jakarta Selatan",
    'jakarta_pusat': "Jakarta Pusat"
}

# Fitur penting saja
important_features = ["RR", "RH_avg", "Tavg"]

@app.route('/', methods=['GET', 'POST'])
def index():
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

            # Ambil hanya 3 fitur penting
            data_input = [
                weather_data['rain_daily'],    # RR
                weather_data['humidity'],      # RH_avg
                weather_data['temp_avg'],      # Tavg
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
        "index.html",
        result=result,
        data=weather_data,
        lokasi_nama=lokasi_nama,
        tanggal_terpilih=tanggal_terpilih
    )

if __name__ == '__main__':
    app.run(debug=True)
