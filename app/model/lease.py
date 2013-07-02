from app import db
from app import app

class Lease(db.Model):
    
    id = db.Column(db.Integer, primary_key = True)
    official_id = db.Column(db.String(32))
    official_name = db.Column(db.String(64))
    nick_name = db.Column(db.String(16))
    contract = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('authenticateduser.id'))
    
    def __repr__(self): # pragma: no cover
        return '<Lease %r>' % (self.body)
        
