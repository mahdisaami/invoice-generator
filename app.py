from flask import Flask, g
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

from configuration import Configuration


invoice_app = Flask(__name__)
invoice_app.config.from_object(Configuration)

db = SQLAlchemy(invoice_app)

migrate = Migrate(invoice_app, db)

bcrypt = Bcrypt(invoice_app)

login_manager = LoginManager(invoice_app)

login_manager.login_view = 'main_pages.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = 'Please log in to access this page.'

from views import bp
invoice_app.register_blueprint(bp)

@login_manager.user_loader
def _user_loader(user_id):
    from models import User
    return User.query.get(int(user_id))


@invoice_app.before_request
def _before_request():
    g.user = current_user
