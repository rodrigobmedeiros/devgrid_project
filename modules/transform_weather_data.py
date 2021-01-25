def filter_weather_data(weather_info):
    """
    This function is responsible to filter weather data obtained from open weather api and
    returns just city_id, temperature and humidity.
    """

    filtered_weather_data = {
        "city_id": weather_info['id'],
        "temperature_celsius":  round(weather_info['main']['temp'] - 273.15, 2),
        "humidity": weather_info['main']['humidity']
    }

    return filtered_weather_data