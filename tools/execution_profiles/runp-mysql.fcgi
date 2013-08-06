#!flask/bin/python

# use mysql
os.environ['DATABASE_URL'] = 'mysql://apps:apps@localhost/apps'

from flup.server.fcgi import WSGIServer
from frmwk import app

if __name__ == '__main__':
    WSGIServer(app).run()
