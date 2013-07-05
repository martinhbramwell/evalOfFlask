from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template
# from flask import flash, redirect, session, url_for, request, g, jsonify

from app.model.lease import Lease

@app.route('/lease')
@app.route('/lease/<nickname>')
@app.route('/lease/<nickname>/<int:page>')
@login_required
def lease(page = 1, nickname = 'Ooops!  Bad'):
	aLease = Lease.query.get(1)
	usr = aLease.nick_name
	a = ['spork', 'eggs', 100, 1234, 9999]
	pyld = {'name': usr, 'lstData': a, 'page': 'Lease'}
	return render_template('lease.html', user = current_user, payload = pyld, posts = a)

