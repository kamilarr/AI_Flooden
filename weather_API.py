import requests

def get_combined_weather(city, api_key, lat, lon):
    """
    Mengambil data cuaca gabungan dari OpenWeatherMap dan NASA POWER API.
    Saat ini hanya ambil data dari OpenWeatherMap untuk demo,
    dan mengembalikan data dengan key yang sesuai untuk model prediksi banjir.
    """
    try:
        # Ambil data cuaca dari OpenWeatherMap
        url_owm = (
            f"http://api.openweathermap.org/data/2.5/weather"
            f"?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        )
        response_owm = requests.get(url_owm)
        response_owm.raise_for_status()
        data_owm = response_owm.json()

        temp_min = data_owm['main']['temp_min']
        temp_max = data_owm['main']['temp_max']
        temp_avg = data_owm['main']['temp']
        humidity = data_owm['main']['humidity']
        rain_1h = data_owm.get('rain', {}).get('1h', 0.0)
        wind_speed = data_owm['wind']['speed']
        wind_deg = data_owm['wind'].get('deg', 0)

        # Dummy data untuk solar radiation dan data NASA POWER
        solar_radiation = 200  # bisa diganti dengan API NASA POWER jika sudah implementasi
        wind_speed_nasa = wind_speed  # samakan sementara

    except Exception as e:
        # Jika ada error saat request API, return default agar Flask tidak error
        print(f"Error saat ambil data cuaca: {e}")
        temp_min = 25
        temp_max = 32
        temp_avg = 28
        humidity = 80
        rain_1h = 0.0
        solar_radiation = 200
        wind_speed = 3
        wind_deg = 0
        wind_speed_nasa = 3

    return {
        'temp_min': temp_min,
        'temp_max': temp_max,
        'temp_avg': temp_avg,
        'humidity': humidity,
        'rain_1h': rain_1h,
        'solar_radiation': solar_radiation,
        'wind_speed': wind_speed,
        'wind_deg': wind_deg,
        'wind_speed_nasa': wind_speed_nasa
    }

