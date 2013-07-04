from app import app
# from app import db, lm, oid, babel

from flask.ext.login import login_required, current_user
# from flask.ext.login import login_user, logout_user

from flask import render_template, jsonify
# from flask import flash, redirect, session, url_for, request, g

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

