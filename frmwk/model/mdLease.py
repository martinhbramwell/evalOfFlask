from frmwk import orm_db
# from frmwk import flask_framework

class Lease(orm_db.Model):
    
    id = orm_db.Column(orm_db.Integer, primary_key = True)
    official_id = orm_db.Column(orm_db.String(32))
    official_name = orm_db.Column(orm_db.String(64))
    nick_name = orm_db.Column(orm_db.String(16))
    contract = orm_db.Column(orm_db.String(140))
    timestamp = orm_db.Column(orm_db.DateTime)
    user_id = orm_db.Column(orm_db.Integer, orm_db.ForeignKey('authenticateduser.id'))
    
    def __repr__(self): # pragma: no cover
        return '<Lease %r>' % (self.official_name)
        
