from flask import Flask , redirect
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from logging import Formatter, DEBUG
from logging.handlers import RotatingFileHandler
from flask_login import LoginManager, login_user, login_required  , logout_user , current_user
from . import config


app = Flask(__name__)
app.config.from_object(config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.session_protection = "strong"
login.login_view = 'auth.index'
login.login_message = '请登入账号再进行下一步操作!'

"""
    app.logger is project logging module
"""

handler = RotatingFileHandler('logs/app.log', maxBytes=10000, backupCount=1)
handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(name)s:%(lineno)d]'
))
handler.setLevel(DEBUG)
app.logger.addHandler(handler)

from .views.auth import auth
app.register_blueprint(auth, url_prefix='/auth')  # auth module blueprint

from .views.index import index
app.register_blueprint(index, url_prefix='/index')  # index module blueprint

from .apis import API
app.register_blueprint(API, url_prefix='/api')

@app.route('/')
def index():
    return redirect('/auth')