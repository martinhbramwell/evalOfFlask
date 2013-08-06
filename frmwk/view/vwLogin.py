from flask import g, url_for, render_template, session, current_app
from flask import redirect, request

from flask.ext.login import current_user, login_user, logout_user

from flask.ext.principal import identity_changed, identity_loaded
from flask.ext.principal import Identity, AnonymousIdentity
from flask.ext.principal import UserNeed, RoleNeed

from frmwk import flask_application, login_manager
from frmwk import openID_service
from frmwk import orm_db

from frmwk.forms.app_forms import LoginForm#, PostForm, SearchForm

from frmwk.model.mdUser import User
from frmwk.model.mdRole import Role

# login stuff ----------------------

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@flask_application.route('/login', methods = ['GET', 'POST'])
@openID_service.loginhandler
def login():

    # Skip this if authenticated already
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
        
    # A login form that uses Flask-WTF
    form = LoginForm()

    # Validate form input
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        
        return openID_service.try_login(form.openid.data, ask_for = ['nickname', 'email'])
        
    # login didn't happen so give them the form (again?)
    return render_template('global/login.html', 
        title = 'Sign In',
        form = form,
        providers = flask_application.config['OPENID_PROVIDERS'])


@openID_service.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash(gettext('Invalid login. Please try again.'))
        return redirect(url_for('login'))
    user = User.query.filter_by(email = resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        nickname = User.make_valid_nickname(nickname)
        nickname = User.make_unique_nickname(nickname)
        anon_role = Role.query.filter_by(id = 'ADMIN').first()
        print 'New user role : ' + anon_role.name
        user = User(nickname = nickname, email = resp.email)
        # 
        orm_db.session.add(user)
        orm_db.session.commit()
        # make the user follow him/herself
        orm_db.session.add(user.follow(user))
        user.takeRole(anon_role)
        orm_db.session.commit()
        
    # check if they want to risk having our app recognize them next time.
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)

    # Keep the user info in the session using Flask-Login
    login_user(user, remember = remember_me)

    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))


    return redirect(request.args.get('next') or url_for('index'))

@flask_application.route('/logout')
def logout():

    # destroy the user's session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # # print ' ** ** ** ' + str(current_app._get_current_object())
    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    # go back to the home page
    return redirect(url_for('index'))
    

@identity_loaded.connect_via(flask_application)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # # print ' $$$$$$$ ' + str(current_user) + ' $$$$$$$ ' + str(current_user.__dict__.keys()) + ' $$$$$$$ '
    
    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        # # print ' - - - needs'
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        # print ' - - - may'
        msg = 'Acts as: ';
        sep = '';
        for role in current_user.roles:
            msg += sep + str(role.name);
            sep = ', ';
            identity.provides.add(RoleNeed(role.id))
        print msg;
# end of login stuff ----------------------


