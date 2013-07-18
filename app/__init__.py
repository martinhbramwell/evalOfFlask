import os
from flask import Flask
from flask import Response

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.mail import Mail 
from flask.ext.babel import Babel, lazy_gettext
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT, MAIL_USERNAME, MAIL_PASSWORD
from momentjs import momentjs

flask_application = Flask(__name__)
flask_application.config.from_object('config')
orm_db = SQLAlchemy(flask_application)

resp = Response

login_manager = LoginManager()
login_manager.init_app(flask_application)
login_manager.login_view = 'login'
login_manager.login_message = lazy_gettext('Please log in to access this page.')

# OpenID service
openID_service = OpenID(flask_application, os.path.join(basedir, 'tmp'))

mail = Mail(flask_application)
babel = Babel(flask_application)

''' Flask - Principal '''
from flask.ext.principal import Principal, Permission, RoleNeed

# load the extension
principals = Principal(flask_application)

# Create a permission with a single Need, in this case a RoleNeed.
comptroller_permission = Permission(RoleNeed('COMPT'))
administrator_permission = Permission(RoleNeed('ADMIN'))

''' Exexcution Profiles '''
if not flask_application.debug and MAIL_SERVER != '':
    import logging
    from logging.handlers import SMTPHandler
    credentials = None
    if MAIL_USERNAME or MAIL_PASSWORD:
        credentials = (MAIL_USERNAME, MAIL_PASSWORD)
    mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@' + MAIL_SERVER, ADMINS, 'microblog failure', credentials)
    mail_handler.setLevel(logging.ERROR)
    flask_application.logger.addHandler(mail_handler)

if not flask_application.debug and os.environ.get('HEROKU') is None:
    import logging
    from logging.handlers import RotatingFileHandler
    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    flask_application.logger.addHandler(file_handler)
    flask_application.logger.setLevel(logging.INFO)
    flask_application.logger.info('microblog startup')

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    flask_application.logger.addHandler(stream_handler)
    flask_application.logger.setLevel(logging.INFO)
    flask_application.logger.info('microblog startup')

flask_application.jinja_env.globals['momentjs'] = momentjs

from app.view import views, overview, vwLogin, vwLease, vwRole, vwUser, vwStake, vwTank, vwWell
# from flask_application import view
from app import model

