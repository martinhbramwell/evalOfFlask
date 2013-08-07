from flask import render_template, flash, redirect, session, url_for, request, g, jsonify
from flask.ext.login import login_user, logout_user, current_user, login_required
from flask.ext.sqlalchemy import get_debug_queries
from flask.ext.babel import gettext

from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed
from flask import current_app


from frmwk import flask_framework, orm_db, login_manager, openID_service, babel
# from frmwk.forms.demo_forms import EditForm
from frmwk.forms.app_forms import LoginForm, PostForm, SearchForm


from frmwk.model.mdUser import User
from frmwk.model.mdRole import Role, ROLE_ANONYMOUS, ROLE_ADMINISTRATOR
from frmwk.model.post import Post

from datetime import datetime
# from frmwk.control.emails import follower_notification
from guess_language import guessLanguage
from frmwk.control.translate import microsoft_translate

from config import POSTS_PER_PAGE, MAX_SEARCH_RESULTS, LANGUAGES, DATABASE_QUERY_TIMEOUT, WHOOSH_ENABLED


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(LANGUAGES.keys())
    
@flask_framework.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        orm_db.session.add(g.user)
        orm_db.session.commit()
        g.search_form = SearchForm()
    g.locale = get_locale()
    g.search_enabled = WHOOSH_ENABLED

@flask_framework.after_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= DATABASE_QUERY_TIMEOUT:
            flask_framework.logger.warning("SLOW QUERY: %s\nParameters: %s\nDuration: %fs\nContext: %s\n" % (query.statement, query.parameters, query.duration, query.context))
    return response

@flask_framework.errorhandler(404)
def internal_error(error):
    return render_template('global/404.html'), 404

@flask_framework.errorhandler(500)
def internal_error(error):
    orm_db.session.rollback()
    return render_template('global/500.html'), 500

@flask_framework.route('/', methods = ['GET', 'POST'])
@flask_framework.route('/index', methods = ['GET', 'POST'])
@flask_framework.route('/index/<int:page>', methods = ['GET', 'POST'])
@login_required
def index(page = 1):
    print 'Home: {}'.format(flask_framework.config['MINE'])
    form = PostForm()
    if form.validate_on_submit():
        language = guessLanguage(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body = form.post.data,
            timestamp = datetime.utcnow(),
            author = g.user,
            language = language)
        orm_db.session.add(post)
        orm_db.session.commit()
        flash(gettext('Your post is now live!'))
        return redirect(url_for('index'))
    posts = g.user.followed_posts().paginate(page, POSTS_PER_PAGE, False)
    return render_template('global/index.html',
        title = 'Home',
        form = form,
        posts = posts)
        
@flask_framework.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t follow yourself!'))
        return redirect(url_for('user', nickname = nickname))
    u = g.user.follow(user)
    if u is None:
        flash(gettext('Cannot follow %(nickname)s.', nickname = nickname))
        return redirect(url_for('user', nickname = nickname))
    orm_db.session.add(u)
    orm_db.session.commit()
    flash(gettext('You are now following %(nickname)s!', nickname = nickname))
    follower_notification(user, g.user)
    return redirect(url_for('user', nickname = nickname))

@flask_framework.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname = nickname).first()
    if user == None:
        flash('User ' + nickname + ' not found.')
        return redirect(url_for('index'))
    if user == g.user:
        flash(gettext('You can\'t unfollow yourself!'))
        return redirect(url_for('user', nickname = nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash(gettext('Cannot unfollow %(nickname)s.', nickname = nickname))
        return redirect(url_for('user', nickname = nickname))
    orm_db.session.add(u)
    orm_db.session.commit()
    flash(gettext('You have stopped following %(nickname)s.', nickname = nickname))
    return redirect(url_for('user', nickname = nickname))

@flask_framework.route('/delete/<int:id>')
@login_required
def delete(id):
    post = Post.query.get(id)
    if post == None:
        flash('Post not found.')
        return redirect(url_for('index'))
    if post.author.id != g.user.id:
        flash('You cannot delete this post.')
        return redirect(url_for('index'))
    orm_db.session.delete(post)
    orm_db.session.commit()
    flash('Your post has been deleted.')
    return redirect(url_for('index'))
    
@flask_framework.route('/search', methods = ['POST'])
@login_required
def search():
    if not g.search_form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query = g.search_form.search.data))

@flask_framework.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Post.query.whoosh_search(query, MAX_SEARCH_RESULTS).all()
    return render_template('global/search_results.html',
        query = query,
        results = results)

@flask_framework.route('/translate', methods = ['POST'])
@login_required
def translate():
    return jsonify({
        'text': microsoft_translate(
            request.form['text'],
            request.form['sourceLang'],
            request.form['destLang']) })


