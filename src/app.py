from flask import Flask
from flask_restful import Resource, Api

from src.resources.Weather import Weather

app = Flask(__name__)
api = Api(app)

# Routes
api.add_resource(Weather, '/weather', '/weather/<string:cityName>')

if __name__ == '__main__':
    app.run(debug=True)
