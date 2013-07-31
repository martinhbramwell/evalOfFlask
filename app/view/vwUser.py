from flask.ext.login import login_required, current_user
from flask.ext.babel import gettext
from flask import render_template, flash, request, redirect, url_for, g

from flask.ext.mail import Message
# from flask.ext.mail import Mail

from app import flask_application, orm_db, mail
from app import administrator_permission

from app.control.utils import pretty_list, ampersandAtEnd

from app.model.mdUser import User
from app.forms.fmUser import UserForm
from app.forms.fmUser import NewUserForm

from app.model.mdRole import Role
from app.model.mdMany2Many import user_roles

from app.forms.app_forms import DeleteRecordsForm

import config 
# POSTS_PER_PAGE, DEFAULT_MAIL_SENDER
# , MAX_SEARCH_RESULTS, LANGUAGES, DATABASE_QUERY_TIMEOUT, WHOOSH_ENABLED

@flask_application.route('/edit/<nickname>', methods = ['GET', 'POST'])
@login_required
def edit(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    print 'Got user : {}'.format(user.id)
    
    if user == None:
        flash(gettext('User %(nickname)s not found.', nickname = nickname))
        return redirect(url_for('index'))

    if administrator_permission.can() or g.user.nickname == nickname:
    
        roleVOs = determineRoles(user)
        form = UserForm(user)
        
        if form.validate_on_submit():
        
            print 'Roles gained : {}.'.format(form.roles.data)
            return saveIt(user, form, 'updated')
            
        else:
        
            form.about_me.data = user.about_me
            form.email.data = user.email
            form.nickname.data = user.nickname
            
        return renderIt('users.html', {'key': 'edit', 'form': form, 'roles': roleVOs, 'user': user})
        
    else:
        flash(gettext('You are not authorised to edit users. You can request permission below.'), 'error')
        return redirect(url_for('users'))
        
    return redirect(url_for('users'))

@flask_application.route('/newuser', methods = ['GET', 'POST'])
@login_required
def newuser():

    if administrator_permission.can():

        user = User()
        roles = Role.query.all()
        form = NewUserForm(user)
        if form.validate_on_submit():
            print 'Roles gained : {}.'.format(form.roles.data)
            return saveIt(user, form)
        return renderIt('users.html', {'key': 'new', 'form': form, 'roles': roles})
    else:
        flash(gettext('You are not authorised to create new users. You can request permission in "Your Profile"'), 'error')
        return redirect(url_for('users'))



@flask_application.route('/user/<nickname>')
@login_required
def user(nickname, page = 1):

    print 'Load : {}'.format(nickname)
    user = User.query.filter_by(nickname = nickname).first()
    
    if user == None:
        flash(gettext('User %(nickname)s not found.', nickname = nickname))
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, config.POSTS_PER_PAGE, False)
    print 'Posts : {}'.format(posts)
    return render_template('user.html',
        user = user,
        posts = posts)

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
            
            return render_template('users_del.html', payload = pyld)
            
        else:
            flash(gettext('You are not authorised to create new users. You can request permission in "Your Profile"'), 'error')
            
    return redirect(url_for('users'))


def determineRoles(user):
    roleVOs = []
    roleIds = []
    for role in user.roles:
        roleIds.append(role.id)
        
    if len(roleIds) < 1:
        roleIds.append('ANON')

    for role in Role.query.all():
        roleVOs.append(type('voRole', (object,), dict(id=role.id, name=role.name, active='active' if (role.id in roleIds) else '')))
       
    return roleVOs

def renderIt(end_point, pyld):
    pyld['pageNum'] = 1
    return renderThem(end_point, pyld)

def renderThem(end_point, pyld):
    pyld['page'] = 'User'
    pyld['records'] = User.query.all() # .paginate(page, config.POSTS_PER_PAGE, False)

    return render_template(end_point, payload = pyld)
    
def saveIt(user, form, op_type='new'):

        user.about_me = form.about_me.data
        user.email = form.email.data
        
#        print 'Will save: {}\n - Notes: {}\n - Email: {}\n - Roles: {}'.format(user.nickname, user.about_me, user.email, form.roles.data)

        if administrator_permission.can():
            user.roles = []
            for aRole in form.roles.data.split(','):
                user.roles.append(Role.query.get(aRole))
        else:
            msg = Message (
                  'Fontus privileges request.'
                , sender=config.DEFAULT_MAIL_SENDER
                , recipients=[g.user.email, config.DEFAULT_MAIL_SENDER]
            )
                        
            msg.body = "{} requests to be allocated {} privileges".format(g.user.nickname, ampersandAtEnd(form.roles.data))
            mail.send(msg)
            
            alert = 'An email has been sent to the site administrators, stating : "{}".'.format(msg.body)
            flash(gettext(alert), 'info')

        if op_type == 'new':
            user.nickname = form.nickname.data
            orm_db.session.add(user)
            
        orm_db.session.commit()
        
        flash(gettext('Your {} user: {}, has been saved.'.format(op_type, user.nickname)), 'success')
        return redirect(url_for('users'))


