from app import flask_application, orm_db
from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from flask import render_template, flash, request, redirect, url_for

from app import administrator_permission

from app.control.utils import pretty_list

from app.model.mdUser import User
from app.forms.fmUser import UserForm
from app.forms.app_forms import DeleteRecordsForm

@flask_application.route('/users')
@flask_application.route('/users/<int:page>')
@login_required
def users(page = 1):
    print 'users or users with ' + str(page)
    return renderThem('users.html', {'pageNum': page}) 

@flask_application.route('/deluser', methods = ['GET', 'POST'])
@login_required
def deluser():
    strIds = request.args.get('id')
    ids = strIds.split(',')
    
    if ids[0]:
    
        if administrator_permission.can():
        
            user_names = []
            user_count = 0
            form = DeleteRecordsForm()
            form.drop.data = strIds
            
            if form.validate_on_submit():
                for id in ids:
                    user = User.query.get(id)
                    user_names.append(user.nickname)
                    print 'Now deleting {}.'.format(user.nickname)
                    orm_db.session.delete(user)
                    orm_db.session.commit()
                    user_count += 1
                if user_count == 1:
                    flash(gettext('Your user: {} has been deleted.'.format(pretty_list(user_names))), 'success')
                else:
                    flash(gettext('Your users: {} have been deleted.'.format(pretty_list(user_names))), 'success')
                return redirect(url_for('users'))

            pyld = {'form': form}
            pyld['page'] = 'User'
            pyld['records'] = []
            
            for id in ids:
                user = User.query.get(id)
                user_names.append(user.nickname)
                print 'Offer to delete {}.'.format(user.nickname)
                pyld['records'].append(user)
                user_count += 1

#            print 'Now we have ' + str(pyld['records'])
            
            return render_template('users_del.html', payload = pyld)
            
        else:
            flash(gettext('You are not authorised to create new users. You can request permission in "Your Profile"'), 'error')
            
    return redirect(url_for('users'))

@flask_application.route('/newuser', methods = ['GET', 'POST'])
@login_required
def newuser():

    if administrator_permission.can():

        user = User()
        form = UserForm(user)
        if form.validate_on_submit():
            return saveIt(user, form)
        return renderIt('users.html', {'key': 'new', 'form': form})
    else:
        flash(gettext('You are not authorised to create new users. You can request permission in "Your Profile"'), 'error')
        return redirect(url_for('users'))

def saveIt(user, form):
        user.nickname = form.nickname.data
        user.about_me = form.about_me.data
        user.email = form.email.data
        
        orm_db.session.add(user)
        orm_db.session.commit()
        flash(gettext('Your new user: {} ({}), has been saved.'.format(user.nickname, user.id)), 'success')
        return redirect(url_for('users'))

def renderIt(end_point, pyld):
    pyld['pageNum'] = 1
    return renderThem(end_point, pyld)

def renderThem(end_point, pyld):
    pyld['page'] = 'User'
    pyld['records'] = User.query.all() # .paginate(page, POSTS_PER_PAGE, False)
    '''
    records = pyld['records']
    for record in records:
        for role in record.roles:
            print ' * * * * * * *' + str(role.name)
    '''
    return render_template(end_point, payload = pyld)
    

