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
def lease(nickname=None, page = 1):
	leases = Lease.query.filter() # .paginate(page, POSTS_PER_PAGE, False)
	form = LeaseForm()
	pyld = {'page': 'Lease', 'key': 'Baby', 'form': form, 'records': leases}
	return render_template('lease.html', payload = pyld)

