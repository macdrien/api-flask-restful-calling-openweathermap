from flask import Flask
from flask_restful import Api

from src.resources.Weather import Weather
from src.resources.Forecast import Forecast

app = Flask(__name__)
api = Api(app)

# Routes
api.add_resource(Weather, '/weather', '/weather/<string:cityName>')
api.add_resource(Forecast, '/forecast', '/forecast/<string:cityName>')

if __name__ == '__main__':
    app.run(debug=True)
