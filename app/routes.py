import os
from functools import wraps
from flask import Flask, session, redirect, url_for, request 
from markupsafe import escape

from app import app
from app.utils import pprint

user_key = os.environ['USER_SECRET_KEY']


def authed(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('key' not in session or session['key'] != user_key):
            return ("no key", 401)        # get user via some ORM system
        return f(*args, **kwargs)
    return wrap

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['key'] = escape(request.form['key'])
        # TODO: handle auth update logic
        # if session['key'] == user_key:
        return redirect('/')
    return '''
        <form method="post">
            <label>key: </label>
            <input type=text name=key>
            <br />
            <input type=submit value=login>
        </form>
    '''


@app.route('/logout')
def logout():
    # remove the key from the session
    session.pop('key', None)
    return redirect(url_for('login'))


# @app.route('/api/v1/devices', methods=['GET'])
# @authed
# def devices():
#     return {
#         'devices': tplink.get_device_list(session['tp_token'])
#     }
