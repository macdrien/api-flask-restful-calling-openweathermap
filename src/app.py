from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, RoleMixin, UserMixin, SQLAlchemyUserDatastore
from flask_security.utils import get_token_status

from src.resources.Weather import Weather
from src.resources.Forecast import Forecast


class ConfigClass(object):
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'

    # Flask-Security settings
    SECURITY_PASSWORD_HASH = 'plaintext'

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users_database.sqlite'  # File-based SQL database


app = Flask(__name__)
app.config.from_object(__name__ + '.ConfigClass')

api = Api(app)

db = SQLAlchemy(app)

roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))


# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)


# Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(email='admin@example.com', password='password')
#     db.session.commit()

@app.after_request
def after_request_func(response):
    print(user_datastore.get_user('admin@example.com').get_auth_token())
    return response


# Routes
api.add_resource(Weather, '/weather', '/weather/<string:cityName>')
api.add_resource(Forecast, '/forecast', '/forecast/<string:cityName>')

if __name__ == '__main__':
    app.run(debug=True)
