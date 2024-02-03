import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_moment import Moment
import yaml
from yaml.loader import SafeLoader

app = Flask(__name__)
login = LoginManager(app)
login.login_view = 'auth.login'
login.login_message = "Пожалуйста, войдите, чтобы открыть эту страницу."

app.config.from_object(Config)
with open('my.yaml') as f:
    my_yaml = yaml.load(f, Loader=SafeLoader)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or my_yaml['secret_key']
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(app.config['BASE_DIR'], my_yaml['db_name'])
    app.config['MAIL_SERVER'] = my_yaml['mail_server']
    app.config['MAIL_USE_TLS'] = my_yaml['mail_use_tls']
    app.config['MAIL_USE_SSL'] = my_yaml['mail_use_ssl']
    app.config['MAIL_PORT'] = my_yaml['mail_port']
    app.config['MAIL_USERNAME'] = my_yaml['mail_username']
    app.config['MAIL_PASSWORD'] = my_yaml['mail_password']
    app.config['MAIL_DEFAULT_SENDER'] = my_yaml['mail_default_sender']
    app.config['ADMINS'] = my_yaml['admins']

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





