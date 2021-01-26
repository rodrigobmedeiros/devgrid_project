from flask import Flask, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from modules.transform_weather_data import filter_weather_data
from modules.set_config import SetConfig
from modules.set_database import SetDatabase
from datetime import datetime
import requests
import time
import sys
import os

def create_app():

    # Load database configuration.
    database_info = SetDatabase()

    # Get database connection string
    db_string = database_info.get_database_string()

    # Load info to connect to open weather api.
    open_weather_api_config = SetConfig()

    app = Flask('__name__')
    app.config['SQLALCHEMY_DATABASE_URI'] = db_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)

    migrate = Migrate(app=app, db=db)

    class WeatherData(db.Model):

        __tablename__ = 'weatherdata'
        id = db.Column(db.Integer, primary_key=True)
        user_defined_id = db.Column(db.Integer, nullable=False)
        request_time = db.Column(db.DateTime, nullable=False)
        weather_info = db.Column(db.JSON, nullable=False)

        def __repr__(self):

            return f'<Weather Data - user_id: {self.user_defined_id} - collect at: {self.request_time}>'


    @app.route('/<user_defined_id>', methods=['GET', 'POST'])
    def insert_weather_data(user_defined_id):

        error = False

        with open(f'user_defined/cities/{user_defined_id}.txt') as f:
            cities = f.read()
        cities_id = cities.split('\n')

        for city_id in cities_id:

            try:

                querystring = {"id": city_id}

                response = requests.request("GET",
                                            open_weather_api_config.url_weather_api,
                                            headers=open_weather_api_config.headers,
                                            params=querystring)

                transformed_weather_data = filter_weather_data(response.json())
                request_time = datetime.now()

                weather_data = WeatherData(user_defined_id=user_defined_id,
                                           request_time=request_time,
                                           weather_info=transformed_weather_data)

                db.session.add(weather_data)
                db.session.commit()

            except:
                error = True
                db.session.rollback()
                print(sys.exc_info())
            finally:
                db.session.close()
            
            # For each loop we're consuming open weather api with a free account what let us make just 10 requests per minute
            # Because of this, the function will wait for 6 seconds until the next request.
            # Whats guarantees at least 10 requests per minute (60 / 6 = 10)
            time.sleep(6)

        if error:
            abort(500)
        else:
            return jsonify({'success': True})

    @app.route('/status/<user_defined_id>')
    def calculate_extraction_progress(user_defined_id):

        with open(f'user_defined/cities/{user_defined_id}.txt') as f:
            cities = f.read()
        cities_id = cities.split('\n')

        collected_cities = WeatherData.query.filter_by(user_defined_id=user_defined_id).all()
        
        progress = (len(collected_cities) / len(cities_id)) * 100

        return jsonify({"Progress Status (%)": round(progress, 2)})


    return app