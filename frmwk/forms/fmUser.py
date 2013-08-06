from flask.ext.wtf import Form, TextField, BooleanField, HiddenField, TextAreaField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

# from frmwk.control.utils import pretty_list

from frmwk.model.mdUser import User

class UserForm(Form):
    nickname = TextField('nickname')
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    email = TextField('email', validators = [Required(), Length(min = 0, max = 120)])
    roles = TextField('roles', validators = [Required()]) # FIXME:
#    roles = HiddenField('roles', validators = [Required()])
    
    def __init__(self, user, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = user.nickname
        
    def validate(self):
        if not Form.validate(self):
            print 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
            return False
        if self.nickname.data == self.original_nickname:
            return True
        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
            self.nickname.errors.append(gettext('This nickname has invalid characters. Please use letters, numbers, dots and underscores only.'))
            return False
        user = User.query.filter_by(nickname = self.nickname.data).first()
        if user != None:
            self.nickname.errors.append(gettext('This nickname is already in use. Please choose another one.'))
            return False
        return True

class NewUserForm(UserForm):
    nickname = TextField('nickname', validators = [Required()])


