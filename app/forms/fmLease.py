from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

import app.model.mdLease

class LeaseForm(Form):
    official_id = TextField('Public Record #', validators = [Required()])
    official_name = TextField('Public Name', validators = [Required()])
    nick_name = TextField('Code Name', validators = [Length(min = 0, max = 16)])
    contract = TextAreaField('Details', validators = [Length(min = 0, max = 140)])

    def __init__(self, lease, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if lease is not None:
            self.the_official_id = lease.official_id
        
        
    def validate(self):
        if not self.official_id.data:
            self.official_id.data = self.the_official_id
        if not Form.validate(self):
            print ' + + + Nope'
            return False
        print ' + + + Yup'
        return True

