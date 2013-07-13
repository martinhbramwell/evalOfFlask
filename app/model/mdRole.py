from app import orm_db

from app.model.mdMany2Many import user_roles

ROLE_ANONYMOUS = 'ANON'
ROLE_ADMINISTRATOR = 'ADMIN'

class Role(orm_db.Model):
    
    id = orm_db.Column(orm_db.String(16), primary_key = True)
    name = orm_db.Column(orm_db.String(64))
    users = orm_db.relationship('User', 
        secondary = user_roles, 
        primaryjoin = (user_roles.c.role_id == id),
        backref = orm_db.backref('role_user', lazy = 'dynamic'), 
        lazy = 'dynamic')
    
    def __repr__(self): # pragma: no cover
        return '<Role %r>' % (self.body)

