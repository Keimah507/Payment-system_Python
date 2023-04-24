from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://app.db'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

login_manager = LoginManager
login_manager.login_view = 'login'
login_manager.init_app(app)
from app import routes, models