from flask.ext.wtf import Form, TextField, BooleanField, HiddenField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

class LoginForm(Form):
    openid = TextField('openid', validators = [Required()])
    remember_me = BooleanField('remember_me', default = False)
    
class PostForm(Form):
    post = TextField('post', validators = [Required()])
    
class DeleteRecordsForm(Form):
#    drop = TextField('drop', validators = [None])
    drop = HiddenField('drop', validators = [Required()])
    
class SearchForm(Form):
    search = TextField('search', validators = [Required()])    

