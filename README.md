# devgrid_project
Repo used to develop a service to get data from Open Weather API.

# What is this.

 The aim idea of this project is to develop an API to get weather data for one or more cities by time. An user pass a list of cities id's to the API and has his data stored into a databse. It's possible to follow to progress of the data extraction.

# Softwares:

## Postgres:

Database was built using postgres, considering that it's an open source object relational database that integrates with python and support ORM development very well. The version used was `13.0`.

## Python:

This API was built using version `3.7.2`

## Flask:

Flask is a python framework used for web development, including API's development. It's widely used and is a very pythonic way to build applications. With flask, was used `flask-sqlalchemy` to connect with the database and abstract SQL concepts and `flask-migrate` to create database version and follow all updates.

# Directory structure

```
├── migrations  
│   └── versions  
|   └── alembic.ini 
|   └── env.py  
|   └── README 
|   └── script.py.mako
├── modules  
|   └── set_config.py 
|   └── set_database.py  
|   └── transform_weather_data.py   
├── user_defined  
|   └── cities  
|       └── 1000.txr 
├── .gitignore  
├── app.py  
├── config.json  
├── LICENSE 
├── README.md
└── requirements.txt
```

# migrations:

Directory responsible to store and control modifications in the databases and tables.

# modules:

Directory with python scripts used to develop the application. 

## set_config:

Define a class to read and alocate log information to connect to open weather API.

`url-weather-api`: "https://community-open-weather-map.p.rapidapi.com/weather",
`headers`:
- `x-rapidapi-key`: "48fb4ad818mshaff694231397f7fp1acde1jsn23c32d3bd5b8",
- `x-rapidapi-host`: "community-open-weather-map.p.rapidapi.com"


## set_database:

Define a class to read and alocate information needed to connect with a postgres database.

`database_info`: 

- `database`: "postgres",
- `user`: "postgres",
- `password`: "draGao01",
- `host`: "localhost",
- `port`: "5432",
- `database_name`: "weatherdb"

## transform_weather_data.api

Define a function responsible to receive complete information for a city and return just city_id, temperature in celsius and humidity.

## user_defined/cities:

Directory used to define a txt file containing all cities that must be collected for each user. The txt file has to have the user_define_is as name. 
Ex: User with user_defined_id equals `1000` has to create the file 1000.txt and fill it with all city_id's.

`1000.txt` - file containing 24 city_id's
```
3439525
3439781
3440645
3442098
3442778
3443341
3442233
3440781
3441572
3441575
3443207
3442546
3441287
3441242
3441686
3440639
3441354
3442057
3442585
3442727
3439705
3441890
3443411
3440054
```

## .gitignore

file user to define what will be tracked and versioned.

## app.py

Python script responsible to define the API, define the endpoints and all connections need to get and post data.

## LICENSE

MIT LICENSE

## README.md

File used to explain the project.

# requirements.txt

Contain all dependencies to be installed.

# How to use

1) Install Python 3.7.2
2) Install Postgres 13.0
3) Install the requirements using the command: `pip install -r requirements.txt`
4) Download the repo and unzip it in a local of preference.
5) create a database table with the sabe name defined into config.json.
6) Update config.json with all your local information.
7) Create a user_defined_id.txt inside `user_defined\cities` with city_id's list.
8) Define flask envinment variables - for `windows`: SET FLASK_APP=app.py
9) run the command: `flask run` in the cmd.
Obs: For more information access the [Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)

# Endpoits

## POST

- `/<user_defined_id>`: Receive an user_defined_id, get all city_id's from user_defined_id.txt file, connect to open weather API, collect information and store into the database.

Ex: Considering localhost 127.0.0.1:5000\
127.0.0.1:5000/1000 is an example where 1000 is a user_defined_id.\

For each city_id, three information are stored in three different columns.
- `user_defined_id`
- `request_time`: containing a timestamp considering the request moment.
- `weather_info`: a JSON containing city_id, temperature in celsius and humiduty

## GET

- `/status/<user_defined_id>`: Receive the user_defind_id and make a query to the database looking for all entries for this user. Return a percentage of progress considering how many cities was collect in comparison of how many city_id's are present into the txt file.

Ex: Considering localhost 127.0.0.1:5000\
127.0.0.1:5000/status/1000 is an example where 1000 is the user_defined_id. A query is done using this id, returning all entries for this specific user. After that a progress percentage is calculated.\

# Opportunity of improvement:

- Today is created an entry for each city. The number of entries can increases very fast considering the increase in the number of users what's not a good thing, thinking about query performance.
- Implement Async calls.
- Include a docker file to setup the environment and run the project, avoiding problems with installation and other dependencies.
