from app import orm_db
from app import app
from config import WHOOSH_ENABLED

class Post(orm_db.Model):
    __searchable__ = ['body']
    
    id = orm_db.Column(orm_db.Integer, primary_key = True)
    body = orm_db.Column(orm_db.String(140))
    timestamp = orm_db.Column(orm_db.DateTime)
    user_id = orm_db.Column(orm_db.Integer, orm_db.ForeignKey('authenticateduser.id'))
    language = orm_db.Column(orm_db.String(5))
    
    def __repr__(self): # pragma: no cover
        return '<Post %r>' % (self.body)
        
if WHOOSH_ENABLED:
    import flask.ext.whooshalchemy as whooshalchemy
    whooshalchemy.whoosh_index(app, Post)
