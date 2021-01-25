from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from modules.set_config import SetConfig
from modules.transform_weather_data import filter_weather_data
import os, sys
import requests
from datetime import datetime

def create_app():

    app = Flask('__name__')
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://postgres:draGao01@localhost:5432/weatherdb"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    db.create_all()

    migrate = Migrate(app=app, db=db)

    class WeatherData(db.Model):

        __tablename__ = 'weatherdata'
        id = db.Column(db.Integer, primary_key=True)
        user_defined_id = db.Column(db.Integer, nullable=False, unique=True)
        request_time = db.Column(db.DateTime, nullable=False)
        weather_info = db.Column(db.String(), nullable=False)

        def __repr__(self):

            return f'<Weather Data - Number: {self.id} - City ID: {self.user_defined_id}>'


    open_weather_api_config = SetConfig()

    @app.route('/<city_id>', methods=['GET'])
    def weather_data(city_id):

        querystring = {"id": city_id}

        response = requests.request("GET",
                                    open_weather_api_config.url_weather_api,
                                    headers=open_weather_api_config.headers,
                                    params=querystring)

        transformed_weather_data = filter_weather_data(response.json())

        return jsonify(transformed_weather_data)

    @app.route('/cities/<city_id>', methods=['GET', 'POST'])
    def insert_weather_data(city_id):

        error = False
        body = {}
        try:

            querystring = {"id": city_id}

            response = requests.request("GET",
                                        open_weather_api_config.url_weather_api,
                                        headers=open_weather_api_config.headers,
                                        params=querystring)

            transformed_weather_data = filter_weather_data(response.json())
            transformed_weather_data_str = str(transformed_weather_data).replace("\'", "\"")
            request_time = datetime.now()

            weather_data = WeatherData(user_defined_id=city_id,
                                       request_time=request_time,
                                       weather_info=transformed_weather_data_str)
            db.session.add(weather_data)
            db.session.commit()

        except:
            error = True
            db.session.rollback()
            print(sys.exc_info())
        finally:
            db.session.close()
        if error:
            abort(500)
        else:
            return jsonify(transformed_weather_data)


    return app