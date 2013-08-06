# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

PROJECT_NAME = 'Warehouseman'

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' },
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]
    
if os.environ.get('DATABASE_URL') is None:
	SQLALCHEMY_DATABASE_URI = 'postgresql://flaskeval:flaskeval@localhost/flaskeval'
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db') + '?check_same_thread=False'
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# email server
MAIL_SERVER         = 'smtp.gmail.com'
MAIL_PORT           = 465
MAIL_USE_SSL        = True
MAIL_USE_TLS        = False
###  MAKE A COPY OF THIS FILE CALLED config.py
###  ENSURE IT IS REFERRED TO IN .gitignore
###  PROVIDE SENSIBLE VALUES FOR THE INDICATED KEY WORDS.
MAIL_USERNAME       = 'your.address@gmail.com'
MAIL_PASSWORD       = 'your gmail password'
DEFAULT_MAIL_SENDER = 'your.address@gmail.com'

# administrator list
# ADMINS = ['you@example.com']

# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = '' # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = '' # enter your MS translator app secret here

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50

