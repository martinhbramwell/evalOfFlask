from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template, request
# from flask import flash, redirect, session, url_for, g, jsonify

from app.model.mdLease import Lease
from app.forms.fmLease import LeaseForm

def renderIt(pyld):
    pyld['pageNum'] = 1
    return renderThem(pyld)

def renderThem(pyld):
    pyld['page'] = 'Lease'
    pyld['records'] = Lease.query.filter() # .paginate(page, POSTS_PER_PAGE, False)
    return render_template('lease.html', payload = pyld)

@app.route('/leases')
@app.route('/leases/<int:page>')
@login_required
def leases(page = 1):
    return renderThem({'pageNum': page})

@app.route('/lease/new', methods = ['GET', 'POST'])
@login_required
def lease():
    return renderIt({'form': LeaseForm(None)})
    
@app.route('/lease/<official_id>', methods = ['GET', 'POST'])
@login_required
def lease(official_id = None):
    lease = Lease.query.filter_by(official_id = official_id).first()
    form = LeaseForm(lease)
    return renderIt({'key': official_id, 'form': form})

