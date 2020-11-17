from flask import request
from flask_restful import Resource
from flask_security import login_required, auth_token_required
from flask_security.utils import logout_user

import requests
import json

with open('common/config.json', 'r') as configFile:
    API_KEY = json.loads(configFile.read())['token']

URL = "https://api.openweathermap.org/data/2.5/forecast"

class Forecast(Resource):
    @auth_token_required
    def get(self, cityName):
        response = requests.get(URL + "?q=" + cityName + "&units=metric&appid=" + API_KEY)
        return json.loads(response.content.decode('utf-8'))
