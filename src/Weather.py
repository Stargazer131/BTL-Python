import requests

data = {
    "weather_key" : "922fa7db5e80194935a053d2bbab7354",
    "ip_key" : "854633293d1654",
    "bot_token" : "5772730359:AAHXZCRZxczH0fiNHLzkVZYmug6Jy4docsc",
    "weather_condition" : {
        "01d" : "sunny",
        "01n" : "sunny",
        "02d" : "sunny",
        "02n" : "sunny",
        "03d" : "cloudy",
        "03n" : "cloudy",
        "04d" : "cloudy",
        "04n" : "cloudy",
        "09d" : "rainy",
        "09n" : "rainy",
        "10d" : "rainy",
        "10n" : "rainy",
        "11d" : "thunderstorm",
        "11n" : "thunderstorm",
        "13d" : "snowy",
        "13n" : "snowy",
        "50d" : "foggy",
        "50n" : "foggy" 
    }
}

WEATHER_KEY = data['weather_key']
IP_KEY = data['ip_key']


def get_current_ip() -> str:
    """
    Returns the current IP
    """
    url = 'https://api.ipify.org'
    return requests.get(url).content.decode('utf-8')


def get_current_location() -> tuple[str, str, float, float]:
    """ 
    Returns the current location in city name, country, latitude and longitude
    """
    url = f'https://ipinfo.io/{get_current_ip()}?token={IP_KEY}'
    data = requests.get(url).json()
    latitude, longitude = [float(x) for x in data['loc'].split(',')]
    return (data['city'], data['country'], latitude, longitude)


def get_city(city: str) -> tuple[str, float, float, str]:
    """
    Returns the current name, latitude, longitude and country of the given city
    """
    url = f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_KEY}'
    data = requests.get(url).json()[0]
    return (data['name'], data['lat'], data['lon'], data['country'])


def get_weather(latitude: float, longitude: float) -> dict:
    """
    Returns data of the weather from the given latitude and longitude
    """
    url = f'https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=metric&exclude=minutely&appid={WEATHER_KEY}'
    return requests.get(url).json()


def get_city_weather(city: str) -> tuple[str, str, dict]:
    """
    Returns its name, country and weather data of the given city
    """
    name, latitude, longitude, country = get_city(city)
    data = get_weather(latitude, longitude)
    return name, country, data


def get_current_location_weather():
    """
    Returns its name, country and weather data of the current location
    """
    name, country, latitude, longitude = get_current_location()
    data = get_weather(latitude, longitude)
    return name, country, data


def main():
    pass


if __name__ == '__main__':
    main()