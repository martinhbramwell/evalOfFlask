from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

from app.model.lease import Lease

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    
class PostForm(Form):
    post = TextField('post', validators = [Required()])
    
class SearchForm(Form):
    search = TextField('search', validators = [Required()])    

class LeaseForm(Form):
    official_id = TextField('Public Record #', validators = [Required()])
    official_name = TextField('Public Name', validators = [Required()])
    nick_name = TextField('Code Name', validators = [Required()])
    contract = TextAreaField('Details', validators = [Length(min = 0, max = 140)])

