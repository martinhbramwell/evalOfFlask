from app import flask_application, orm_db
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from flask import render_template, flash, request, redirect, url_for

from app import administrator_permission
from flask import Response

from app.model.mdUser import User
from app.forms.fmUser import UserForm

@flask_application.route('/users')
@flask_application.route('/users/<int:page>')
@login_required
def users(page = 1):
    print 'users or users with ' + str(page)
    return renderThem({'pageNum': page}) 

@flask_application.route('/newuser', methods = ['GET', 'POST'])
@login_required
def newuser():
    print 'newuser'
    if administrator_permission.can():

        user = User()
        form = UserForm(user)
        if form.validate_on_submit():
            print 'saving * * * * '
            return saveIt(user, form)
        return renderIt({'key': 'new', 'form': form})
    else:
        flash(gettext('You are not authorised to create new users. You can request permission in "Your Profile"'), 'error')
        return redirect(url_for('users'))

def saveIt(user, form):
        user.nick_name = form.nick_name.data
        user.official_id = form.official_id.data
        user.official_name = form.official_name.data
        orm_db.session.add(user)
        orm_db.session.commit()
        flash(gettext('Your changes have been saved.'), 'success')
        return redirect(url_for('users'))

def renderIt(pyld):
    pyld['pageNum'] = 1
    return renderThem(pyld)

def renderThem(pyld):
    pyld['page'] = 'User'
    pyld['records'] = User.query.all() # .paginate(page, POSTS_PER_PAGE, False)
    records = pyld['records']
    for record in records:
        for role in record.roles:
            print ' * * * * * * *' + str(role.name)
    return render_template('users.html', payload = pyld)
    

