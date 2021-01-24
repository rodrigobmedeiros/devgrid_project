from flask import Flask, jsonify
from modules.set_config import SetConfig
import os

def create_app():

    app = Flask('__name__')

    open_weather_api_config = SetConfig()
    print(open_weather_api_config.url_weather_api)
    print(open_weather_api_config.x_rapidapi_key)
    print(open_weather_api_config.x_rapidapi_host)


    @app.route('/')
    def test_endpoint():

        
        return jsonify({'name': 'Rodrigo'})







    return app