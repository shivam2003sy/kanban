import os
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

from flask_restful import Api
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)
app.config.from_object('app.config.Config')

db = SQLAlchemy(app) # flask-sqlalchemy
bc = Bcrypt(app) # flask-bcrypt

lm = LoginManager() # flask-loginmanager
lm.init_app(app)       # init the login manager


# flask restfull api
api = Api(app)
# Setup database
@app.before_first_request
def initialize_database():
    db.create_all()

# Import routing, models and Start the App
from app import views, models , apiendpoints
