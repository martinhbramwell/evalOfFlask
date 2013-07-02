from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template
# from flask import flash, redirect, session, url_for, request, g, jsonify

@app.route('/lease')
@app.route('/lease/<nickname>')
@app.route('/lease/<nickname>/<int:page>')
@login_required
def lease(page = 1):
    # user = User.query.filter_by(nickname = nickname).first()
    # if user == None:
    #     flash(gettext('User %(nickname)s not found.', nickname = nickname))
    #     return redirect(url_for('index'))
    usr = 'Billy Bob'
    a = ['spork', 'eggs', 100, 1234, 9999]
    pyld = {'name': usr, 'lstData': a}
    return render_template('lease.html',
        user = current_user, payload = pyld)


