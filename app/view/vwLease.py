from app import app, orm_db
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask.ext.babel import gettext

from flask import render_template, flash, request, redirect, url_for
# from flask import flash, session, g, jsonify

from app.model.mdLease import Lease
from app.forms.fmLease import LeaseForm

@app.route('/leases')
@app.route('/leases/<int:page>')
@login_required
def leases(page = 1):
    print 'leases or leases with ' + str(page)
    return renderThem({'pageNum': page}) 

@app.route('/newlease', methods = ['GET', 'POST'])
@login_required
def newlease():
    print 'newlease'
    lease = Lease()
    form = LeaseForm(lease)
    if form.validate_on_submit():
        print 'saving * * * * '
        return saveIt(lease, form)
    return renderIt({'key': 'new', 'form': form})
    
@app.route('/lease/<official_id>', methods = ['GET', 'POST'])
@login_required
def lease(official_id = None):
    print 'lease/id with ' + str(official_id)
    lease = Lease.query.filter_by(official_id = official_id).first()
    form = LeaseForm(lease)
    if form.validate_on_submit():
        print 'saving * * * * '
        return saveIt(lease, form)
    elif request.method != "POST":
        form.nick_name.data = lease.nick_name
        form.official_id.data = lease.official_id
        form.official_name.data = lease.official_name
    return renderIt({'key': official_id, 'form': form})

def saveIt(lease, form):
        lease.nick_name = form.nick_name.data
        lease.official_id = form.official_id.data
        lease.official_name = form.official_name.data
        orm_db.session.add(lease)
        orm_db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('lease', official_id = lease.official_id))

def renderIt(pyld):
    pyld['pageNum'] = 1
    return renderThem(pyld)

def renderThem(pyld):
    pyld['page'] = 'Lease'
    pyld['records'] = Lease.query.filter() # .paginate(page, POSTS_PER_PAGE, False)
    return render_template('lease.html', payload = pyld)


