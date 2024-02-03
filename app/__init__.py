import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)
moment = Moment(app)

from app.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from app.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

from app.main import bp as main_bp
app.register_blueprint(main_bp)

from app.crud import bp as crud_bp
app.register_blueprint(crud_bp, url_prefix='/crud')

from app import models

basedir = os.path.abspath(os.path.dirname(__file__))
static = os.path.join(basedir, 'static')
app.config['UPLOAD_SAVE'] = os.path.join(static, app.config['UPLOAD'])





