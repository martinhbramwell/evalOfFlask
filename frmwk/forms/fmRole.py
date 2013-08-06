from flask.ext.wtf import Form, TextField, BooleanField, TextAreaField
from flask.ext.wtf import Required, Length
from flask.ext.babel import gettext

from frmwk.model.mdRole import Role

class RoleForm(Form):
    name = TextField('name', validators = [Required()])
    role_id = TextField('role_id', validators = [Required(), Length(min = 3, max = 8)])
    
    def __init__(self, original_role, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.the_original_id = ""
        print ' . . . . . . . . . . . . . . .' + str(original_role.id)
        if original_role.id is not None:
            self.the_original_id = original_role.id.upper()
        
    def validate(self):
        print 'A'
        if not self.role_id.data:
            self.role_id.data = self.the_original_id
        self.role_id.data = self.role_id.data.upper()
        if not Form.validate(self):
            print 'B'
            return False
        if self.role_id.data == self.the_original_id:
            print 'C1 ' + str(self.role_id.data)
            return True
        print 'D'
        role = Role.query.filter_by(name = self.name.data).first()
        print 'E'
        if role != None:
            print 'F'
            self.name.errors.append(gettext('This nickname is already in use. Please choose another one.'))
            return False
        return True


