from flask import Flask, jsonify
from modules.set_config import SetConfig
from modules.transform_weather_data import filter_weather_data
import os
import requests

def create_app():

    app = Flask('__name__')

    open_weather_api_config = SetConfig()

    @app.route('/')
    def test_endpoint():
        
        return jsonify({'name': 'Rodrigo'})


    @app.route('/<city_id>', methods=['GET'])
    def weather_data(city_id):

        querystring = {"id": city_id}

        response = requests.request("GET",
                                    open_weather_api_config.url_weather_api,
                                    headers=open_weather_api_config.headers,
                                    params=querystring)

        transformed_weather_data = filter_weather_data(response.json())

        return jsonify(transformed_weather_data)

    return app