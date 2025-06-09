import requests
import datetime

def get_combined_weather(lokasi, api_key, lat, lon, tanggal=None):
    today_str = datetime.date.today().isoformat()

    # Jika tidak ada tanggal yang dimasukkan, default ke hari ini
    if tanggal is None:
        tanggal = today_str
    else:
        tanggal = tanggal[:10]  # format YYYY-MM-DD

    try:
        if tanggal == today_str:
            # 🔵 OpenWeatherMap untuk hari ini (real-time)
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
            rain_daily = data_owm.get('rain', {}).get('24h', data_owm.get('rain', {}).get('1h', 0.0) * 24)
            wind_speed = data_owm['wind']['speed']
            wind_deg = data_owm['wind'].get('deg', 0)

            # Hitung durasi penyinaran
            sunrise_ts = data_owm['sys']['sunrise']
            sunset_ts = data_owm['sys']['sunset']
            sunrise = datetime.datetime.fromtimestamp(sunrise_ts)
            sunset = datetime.datetime.fromtimestamp(sunset_ts)
            daylight_hours = (sunset - sunrise).total_seconds() / 3600

            # Koreksi mendung
            cloudiness = data_owm.get('clouds', {}).get('all', 0)
            if cloudiness > 75:
                daylight_hours *= 0.7

            wind_speed_nasa = wind_speed

        else:
            # 🟠 NASA POWER API untuk tanggal selain hari ini
            tanggal_nasa = tanggal.replace("-", "")
            url_nasa = (
                f"https://power.larc.nasa.gov/api/temporal/daily/point"
                f"?parameters=T2M,T2M_MAX,T2M_MIN,RH2M,WS2M,PRECTOTCORR,ALLSKY_SFC_SW_DWN"
                f"&start={tanggal_nasa}&end={tanggal_nasa}"
                f"&latitude={lat}&longitude={lon}&format=JSON"
            )
            response_nasa = requests.get(url_nasa)
            response_nasa.raise_for_status()
            data = response_nasa.json()["properties"]["parameter"]

            temp_min = data["T2M_MIN"][tanggal_nasa]
            temp_max = data["T2M_MAX"][tanggal_nasa]
            temp_avg = data["T2M"][tanggal_nasa]
            humidity = data["RH2M"][tanggal_nasa]
            rain_daily = data["PRECTOTCORR"][tanggal_nasa]
            daylight_hours = data["ALLSKY_SFC_SW_DWN"][tanggal_nasa] / 0.2  # pendekatan kasar
            wind_speed = data["WS2M"][tanggal_nasa]
            wind_deg = 0  # NASA tidak punya data arah angin
            wind_speed_nasa = wind_speed

    except Exception as e:
        print(f"Error saat ambil data cuaca: {e}")
        # Default/fallback values
        temp_min = 25
        temp_max = 32
        temp_avg = 28
        humidity = 80
        rain_daily = 0.0
        daylight_hours = 8
        wind_speed = 3
        wind_deg = 0
        wind_speed_nasa = 3

    return {
        'temp_min': temp_min,
        'temp_max': temp_max,
        'temp_avg': temp_avg,
        'humidity': humidity,
        'rain_1h': rain_daily,
        'daylight_hours': daylight_hours,
        'wind_speed': wind_speed,
        'wind_deg': wind_deg,
        'wind_speed_nasa': wind_speed_nasa
    }
