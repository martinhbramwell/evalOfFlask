from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template
# from flask import flash, redirect, session, url_for, request, g, jsonify
@app.route('/appl')
@app.route('/appl/<int:page>')
@login_required
def appl(page = 1):
    # user = User.query.filter_by(nickname = nickname).first()
    # if user == None:
    #     flash(gettext('User %(nickname)s not found.', nickname = nickname))
    #     return redirect(url_for('index'))
    return render_template('appl.html',
        user = current_user)


