import requests
import datetime

def get_combined_weather(lokasi, api_keys, lat, lon, tanggal=None):
    today_str = datetime.date.today().isoformat()

    if tanggal is None:
        tanggal = today_str
    else:
        tanggal = tanggal[:10]

    try:
        if tanggal == today_str:
            # 🔵 Hari ini → pakai OpenWeather
            url_owm = (
                f"http://api.openweathermap.org/data/2.5/weather"
                f"?lat={lat}&lon={lon}&appid={api_keys['openweather']}&units=metric"
            )
            response_owm = requests.get(url_owm)
            response_owm.raise_for_status()
            data_owm = response_owm.json()

            temp_min = data_owm['main']['temp_min']
            temp_max = data_owm['main']['temp_max']
            temp_avg = data_owm['main']['temp']
            humidity = data_owm['main']['humidity']
            rain_daily = data_owm.get('rain', {}).get('1h', 0.0) * 24  # dihitung 24 jam
            wind_speed = data_owm['wind']['speed']
            wind_deg = data_owm['wind'].get('deg', 0)

            # Estimasi durasi sinar matahari
            sunrise = datetime.datetime.fromtimestamp(data_owm['sys']['sunrise'])
            sunset = datetime.datetime.fromtimestamp(data_owm['sys']['sunset'])
            daylight_hours = (sunset - sunrise).total_seconds() / 3600

            cloudiness = data_owm.get('clouds', {}).get('all', 0)
            if cloudiness > 75:
                daylight_hours *= 0.7

        else:
            # 🟡 Hari selain hari ini → pakai Visual Crossing
            url_vc = (
                f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/"
                f"{lat},{lon}/{tanggal}?unitGroup=metric&key={api_keys['visualcrossing']}&include=days,hours"
            )
            response_vc = requests.get(url_vc)
            response_vc.raise_for_status()
            data_vc = response_vc.json()["days"][0]

            temp_min = data_vc["tempmin"]
            temp_max = data_vc["tempmax"]
            temp_avg = data_vc["temp"]
            humidity = data_vc["humidity"]
            rain_daily = data_vc.get("precip", 0.0)
            daylight_hours = data_vc.get("hoursOfSun", 12)
            wind_speed = data_vc["windspeed"]
            wind_deg = data_vc.get("winddir", 0)

        data_valid = True

    except Exception as e:
        print(f"⚠️ Gagal ambil data cuaca: {e}")
        # 🌤 Default berdasarkan data historis Jakarta
        temp_min = 0
        temp_max = 0
        temp_avg = 0
        humidity = 0
        rain_daily = 0
        daylight_hours = 0
        wind_speed = 0
        wind_deg = 0
        data_valid = False

    return {
        'temp_min': temp_min,
        'temp_max': temp_max,
        'temp_avg': temp_avg,
        'humidity': humidity,
        'rain_daily': rain_daily,
        'daylight_hours': daylight_hours,
        'wind_speed': wind_speed,
        'wind_deg': wind_deg,
        'wind_speed': wind_speed,  # untuk ff_x dan ff_avg
        'data_valid': data_valid
    }
