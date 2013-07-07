from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    
class PostForm(Form):
    post = TextField('post', validators = [Required()])
    
class SearchForm(Form):
    search = TextField('search', validators = [Required()])    

