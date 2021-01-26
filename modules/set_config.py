import json

class SetConfig():
    """
    class responsible to load configuration info from config.json file
    """
    def __init__(self):

        self.url_weather_api = None
        self.headers = None
        self.read_config_file()

    def read_config_file(self):

        with open('./config.json') as config_file:

            config_info = json.load(config_file)

        self.url_weather_api = config_info["url-weather-api"]
        self.headers = config_info["headers"]

        return None