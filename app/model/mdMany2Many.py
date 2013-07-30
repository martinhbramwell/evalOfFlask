from app import orm_db

user_roles = orm_db.Table('user_roles',
      orm_db.Column('role_id', orm_db.String(16), orm_db.ForeignKey('role.id'))
    , orm_db.Column('user_id', orm_db.Integer, orm_db.ForeignKey('authenticateduser.id'))
)

followers = orm_db.Table('followers',
    orm_db.Column('follower_id', orm_db.Integer, orm_db.ForeignKey('authenticateduser.id')),
    orm_db.Column('followed_id', orm_db.Integer, orm_db.ForeignKey('authenticateduser.id'))
)


