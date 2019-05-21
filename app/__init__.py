from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
# db.engine.execute("PRAGMA foreign_keys = ON")
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'

if not app.debug:
    if 'MAIL_SERVER' in app.config:
        _host = app.config['MAIL_SERVER']
        auth = None
        if 'MAIL_USERNAME' in app.config and 'MAIL_PASSWORD' in app.config:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        _secure = None
        if 'MAIL_USE_TLS' in app.config:
            _secure = app.config['MAIL_USE_TLS']
        mail_handler = SMTPHandler(mailhost=(_host, app.config['MAIL_PORT']),
                                   fromaddr='no-reply@' + str(_host),
                                   toaddrs=app.config['ADMINS'],
                                   subject='Microblog Failure',
                                   credentials=auth, secure=_secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
from app import routes, models, errors
