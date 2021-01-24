import json

class SetConfig():

    def __init__(self):

        self.url_weather_api = None
        self.x_rapidapi_key = None
        self.x_rapidapi_host = None
        self.read_config_file()

    def read_config_file(self):

        with open('./config.json') as config_file:

            config_info = json.load(config_file)

        self.url_weather_api = config_info["url-weather-api"]
        self.x_rapidapi_key = config_info["headers"]["x-rapidapi-key"]
        self.x_rapidapi_host = config_info["headers"]["x-rapidapi-host"]
