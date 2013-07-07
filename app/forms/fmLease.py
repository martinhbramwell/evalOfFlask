from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

import app.model.mdLease

class LeaseForm(Form):
    official_id = TextField('Public Record #', validators = [Required()])
    official_name = TextField('Public Name', validators = [Required()])
    nick_name = TextField('Code Name', validators = [Length(min = 0, max = 16)])
    contract = TextAreaField('Details', validators = [Length(min = 0, max = 140)])

