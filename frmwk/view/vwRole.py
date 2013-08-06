from frmwk import flask_application, orm_db
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from flask import render_template, flash, request, redirect, url_for, g

from frmwk import administrator_permission
# from flask import Response

from frmwk.model.mdRole import Role
from frmwk.forms.fmRole import RoleForm

@flask_application.route('/roles')
@flask_application.route('/roles/<int:page>')
@login_required
def roles(page = 1):
    print 'roles or roles with ' + str(page)
    return renderThem({'pageNum': page}) 

@flask_application.route('/newrole', methods = ['GET', 'POST'])
@login_required
def newrole():
    print 'newrole'
    if administrator_permission.can():

        role = Role()
        form = RoleForm(role)
        if form.validate_on_submit():
            print 'saving * * * * '
            return saveIt(role, form)
        return renderIt({'key': 'new', 'form': form})
    else:
        flash(gettext('You are not authorised to create new roles. You can request permission below.'), 'error')
        return redirect(url_for('roles'))

@flask_application.route('/role/<role_id>', methods = ['GET', 'POST'])
@login_required
def role(role_id = None):
    print 'role/id with ' + str(role_id)
    if administrator_permission.can():

        role = Role.query.filter_by(id = role_id).first()
        form = RoleForm(role)
        if form.validate_on_submit():
            print "Saving {} with key {}.".format(form.name.data, form.role_id.data)
            return saveIt(role, form)
        elif request.method != "POST":
            form.name.data = role.name
            form.role_id.data = role.id
        return renderIt({'key': role_id, 'form': form})
        
    else:
        flash(gettext('You are not authorised to edit roles. You can request permission below.'), 'error')
        return redirect(url_for('edit', nickname = g.user.nickname))


def saveIt(role, form):
        role.name = form.name.data
        role.id = form.role_id.data
        orm_db.session.add(role)
        orm_db.session.commit()
        flash(gettext('Your changes have been saved.'), 'success')
        return redirect(url_for('roles'))

def renderIt(pyld):
    pyld['pageNum'] = 1
    return renderThem(pyld)

def renderThem(pyld):
    pyld['page'] = 'Role'
    pyld['records'] = Role.query.all() # .paginate(page, POSTS_PER_PAGE, False)
    records = pyld['records']
    return render_template('role.html', payload = pyld)
    

