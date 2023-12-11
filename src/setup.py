from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from os import environ

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = environ.get('JWT_KEY') 

# set the database URI via SQLAlchemy,
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://eat_the_frog_dev:spameggs123@127.0.0.1:5432/eat_the_frog_db'

# create the database object
db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)