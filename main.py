import requests

url = "https://community-open-weather-map.p.rapidapi.com/weather"

querystring = {"id":"3439525"}

headers = {
    'x-rapidapi-key': "48fb4ad818mshaff694231397f7fp1acde1jsn23c32d3bd5b8",
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

teste = response.json()

print(teste['main']['temp'])
print(type(teste))