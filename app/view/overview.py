from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template, jsonify, g
# from flask import flash, redirect, session, url_for, request

# from app.forms.app_forms import LeaseForm
from app.forms.fmLease import LeaseForm

'''
@app.route('/lease', methods = ['GET', 'POST'])
@login_required
def editLease():
		form = LeaseForm(g.user.nickname)
		if form.validate_on_submit():
		    g.user.nickname = form.nickname.data
		    g.user.about_me = form.about_me.data
		    orm_db.session.add(g.user)
		    orm_db.session.commit()
		    flash(gettext('Your changes have been saved.'))
		    return redirect(url_for('edit'))
		elif request.method != "POST":
		    form.nickname.data = g.user.nickname
		    form.about_me.data = g.user.about_me
		return render_template('lease.html',
		    form = form)
    return render_template('lease.html')
'''

@app.route('/v1/appl')
@app.route('/v1/appl/<int:page>')
def api_appl(page = 1, internal = False):
    usr = 'Willy'
    a = ['spam', 'eggs', 100, 1234, 9999]
    pyld = {'name': usr, 'lstData': a}
    if internal:
    	return pyld
    return jsonify(pyld)

@app.route('/appl')
@app.route('/appl/<int:page>')
@login_required
def appl(page = 1):
    pyld = api_appl(page, True)
    return render_template('appl.html',
        user = current_user, payload = pyld)


