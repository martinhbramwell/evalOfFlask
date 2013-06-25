from app import db
from app import app
from config import WHOOSH_ENABLED

class Post(db.Model):
    __searchable__ = ['body']
    
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('authenticateduser.id'))
    language = db.Column(db.String(5))
    
    def __repr__(self): # pragma: no cover
        return '<Post %r>' % (self.body)
        
if WHOOSH_ENABLED:
    import flask.ext.whooshalchemy as whooshalchemy
    whooshalchemy.whoosh_index(app, Post)
