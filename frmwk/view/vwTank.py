from frmwk import flask_framework
# from frmwk import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template
# from flask import flash, redirect, session, url_for, request, g, jsonify

from frmwk.model.mdLease import Lease

@flask_framework.route('/tank')
@flask_framework.route('/tank/<nickname>')
@flask_framework.route('/tank/<nickname>/<int:page>')
@login_required
def tank(page = 1, nickname = 'Ooops!  Bad'):
    aLease = Lease.query.get(2)
    usr = aLease.nick_name
    a = ['spork', 'eggs', 100, 1234, 9999]
    pyld = {'key': usr, 'lstData': a, 'page': 'Tank'}
    return render_template('tank.html', user = current_user, payload = pyld, posts = a)

