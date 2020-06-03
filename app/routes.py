import os
from functools import wraps
from flask import Flask, session, redirect, url_for, request 
from markupsafe import escape

from app import app

auth0_client_id = os.environ['AUTH0_CLIENT_ID']

@app.route('/client-info', methods=['GET'])
def handle_client_info():
    """Returns the auth0 client info"""
    return  {
        'domain': 'travisshears-dev.eu.auth0.com',
        'client_id': auth0_client_id
    }


# def authed(f):
#     @wraps(f)
#     def wrap(*args, **kwargs):
#         if ('key' not in session or session['key'] != user_key):
#             return ("no key", 401)        # get user via some ORM system
#         return f(*args, **kwargs)
#     return wrap

# @app.route('/client-info', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         session['key'] = escape(request.form['key'])
#         # TODO: handle auth update logic
#         # if session['key'] == user_key:
#         return redirect('/')
#     return '''
#         <form method="post">
#             <label>key: </label>
#             <input type=text name=key>
#             <br />
#             <input type=submit value=login>
#         </form>
#     '''


# @app.route('/logout')
# def logout():
#     # remove the key from the session
#     session.pop('key', None)
#     return redirect(url_for('login'))


# @app.route('/api/v1/devices', methods=['GET'])
# @authed
# def devices():
#     return {
#         'devices': tplink.get_device_list(session['tp_token'])
#     }
