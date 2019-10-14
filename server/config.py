from flask_login import LoginManager
from flask_restful import Api
from flask import Flask
from flask_cors import CORS


# app = Flask(__name__)
app = Flask(__name__)
CORS(app)

# =================for testing=================
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'some-secret-string'

api = Api(app)