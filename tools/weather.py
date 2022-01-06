import requests
import logging

from config import OPENWEATHER_API

base_url = "https://api.openweathermap.org/data/2.5/weather?"

CODE_SUCCESS = "200"
CODE_INVALID_API_KEY = "401"
CODE_CITY_NOT_FOUND = "404"


class InvalidApiKeyError(ValueError):
    pass


def get_weather(city_name: str):
    complete_url = base_url + "appid=" + OPENWEATHER_API + \
        "&q=" + city_name + "&units=metric"

    response = requests.get(complete_url)
    json_full_object = response.json()
    logging.debug(str(json_full_object))

    response_code = str(json_full_object.get("cod"))

    if response_code == CODE_SUCCESS:
        return __convert_json_to_weather_string(json_full_object)
    elif response_code == CODE_INVALID_API_KEY:
        raise InvalidApiKeyError
    elif response_code == CODE_CITY_NOT_FOUND:
        return "City " + f"<b>{city_name}</b>" + \
               " is not found, try a different city name. \n" \
               "example usage: /weather moscow"


def __convert_json_to_weather_string(weather_json):
    json_main_object = weather_json.get("main")
    current_temperature = json_main_object.get("temp")
    current_pressure = json_main_object.get("pressure")
    current_humidity = json_main_object.get("humidity")

    json_weather_object = weather_json.get("weather")
    weather_description = json_weather_object[0].get("description")

    city_name = weather_json.get("name")
    json_system_info = weather_json.get("sys")
    country_code = json_system_info.get("country")

    return "City: " + city_name + \
           "\nCountry code: " + country_code + \
           "\nCurrent temperature: " + str(current_temperature) + " °C" + \
           "\nCurrent pressure: " + str(current_pressure) + " hPa" + \
           "\nHumidity: " + str(current_humidity) + "%" + \
           "\nDescription: " + str(weather_description)
