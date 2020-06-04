import os
from functools import wraps

from flask import g
from markupsafe import escape

from app.auth import requires_auth, AUTH0_DOMAIN, API_AUDIENCE
from app import app

auth0_client_id = os.environ['AUTH0_CLIENT_ID']
api_prefix = '/api/run/v1'

@app.route(f'{api_prefix}/client-info', methods=['GET'])
def handle_client_info():
    """Returns the auth0 client info"""
    return  {
        'domain': AUTH0_DOMAIN,
        'client_id': auth0_client_id,
        'audience': API_AUDIENCE
    }

@app.route(f'{api_prefix}/user', methods=['GET'])
@requires_auth
def handle_get_user():
    """Returns an existing user or creates one"""
    return g.user



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
