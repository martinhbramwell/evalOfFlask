from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template
# from flask import flash, redirect, session, url_for, request, g, jsonify

from app.model.mdLease import Lease
from app.forms.fmLease import LeaseForm

@app.route('/lease', methods = ['GET', 'POST'])
@app.route('/lease/<nickname>', methods = ['GET', 'POST'])
@app.route('/lease/<nickname>/<int:page>', methods = ['GET', 'POST'])
@login_required
def lease(page = 1, nickname = 'Ooops!  Bad'):
	aLease = Lease.query.get(1)
	unique = aLease.nick_name
	form = LeaseForm()
	a = ['spork', 'eggs', 100, 1234, 9999]
	pyld = {'key': unique, 'page': 'Lease', 'form': form}
	return render_template('lease.html', user = current_user, payload = pyld, posts = a)

