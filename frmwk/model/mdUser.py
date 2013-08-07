from hashlib import md5
from frmwk import orm_db
from frmwk import flask_framework
import re

from frmwk.model.post import Post
from frmwk.model.mdRole import Role
from frmwk.model.mdMany2Many import user_roles, followers

class User(orm_db.Model):
    __tablename__ = 'authenticateduser'
    id = orm_db.Column(orm_db.Integer, primary_key = True)
    nickname = orm_db.Column(orm_db.String(64), unique = True)
    email = orm_db.Column(orm_db.String(120), index = True, unique = True)
    roles = orm_db.relationship('Role', 
        secondary = user_roles, 
        primaryjoin = (user_roles.c.user_id == id),
        backref = orm_db.backref('user_role', lazy = 'dynamic'), 
        lazy = 'dynamic')

    posts = orm_db.relationship('Post', backref = 'author', lazy = 'dynamic')
    about_me = orm_db.Column(orm_db.String(512))
    last_seen = orm_db.Column(orm_db.DateTime)
    followed = orm_db.relationship('User', 
        secondary = followers, 
        primaryjoin = (followers.c.follower_id == id), 
        secondaryjoin = (followers.c.followed_id == id), 
        backref = orm_db.backref('followers', lazy = 'dynamic'), 
        lazy = 'dynamic')

    @staticmethod
    def make_valid_nickname(nickname):
        return re.sub('[^a-zA-Z0-9_\.]', '', nickname)

    @staticmethod
    def make_unique_nickname(nickname):
        if User.query.filter_by(nickname = nickname).first() == None:
            return nickname
        version = 2
        while True:
            new_nickname = nickname + str(version)
            if User.query.filter_by(nickname = new_nickname).first() == None:
                break
            version += 1
        return new_nickname
        
# Roles methods
    def takeRole(self, role):
        if not self.has_role(role):
            self.roles.append(role)
            print 'Took role : ' + role.name
            return self
            
    def leaveRole(self, role):
        if self.has_role(role):
            self.roles.remove(role)
            return self
            
    def has_named_role(self, roleKey):
        return self.roles.filter(user_roles.c.role_id == roleKey).count() > 0

    def has_role(self, role):
        return self.roles.filter(user_roles.c.role_id == role.id).count() > 0

    def allowed_roles(self):
        return Role.query.join(user_roles,
                (user_roles.c.role_id == Role.id)
            ).filter(user_roles.c.user_id == self.id)  

# Authentication methods
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email).hexdigest() + '?d=mm&s=' + str(size)

# Follower methods---

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self
            
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self
            
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

    def __repr__(self): # pragma: no cover
        return '<User %r>' % (self.nickname)    

