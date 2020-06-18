import os
from functools import wraps
from pprint import pprint

from flask import g, request
from markupsafe import escape
from mongoengine import ValidationError

from app.auth import requires_auth, AUTH0_DOMAIN, API_AUDIENCE, delete_auth0_user
from app.user import User, UserNotFound
from app import app

auth0_client_id = os.environ['AUTH0_BROWSER_CLIENT_ID']
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
def handle_user_get():
    """Returns an existing user or creates one"""
    try:
        auth0_id = g.user['sub']
        user = User(auth0_id)
        return user.dump()
    except Exception as e:
        return default_error_responce(e)

@app.route(f'{api_prefix}/user', methods=['DELETE'])
@requires_auth
def handle_user_delete():
    """Deletes an existing user"""
    try:
        auth0_id = g.user['sub']
        user = User(auth0_id, no_create=True)
        user.delete()
        extra_info = delete_auth0_user(auth0_id)
        return {
            'status': 'success',
            'extra_info': extra_info
        }
    except UserNotFound as e:
        return user_not_found_responce(e)
    except Exception as e:
        return default_error_responce(e)

@app.route(f'{api_prefix}/user', methods=['PATCH'])
@requires_auth
def handle_user_patch():
    """Updates fields on a user"""
    try:
        req = request.json
        auth0_id = g.user['sub']
        user = User(auth0_id, no_create=True)
        user.update(req['fields'])
    except ValidationError as e:
        return ({
            'status': 'error', 
            'reason': str(e)
        }, 400)
    except KeyError as e:
        return ({
            'status': 'error', 
            'reason': f'cant save key {e}'
        }, 400)
    except UserNotFound as e:
        return user_not_found_responce(e)
    except Exception as e:
        return default_error_responce(e)
    return {
        'status': 'success'
    }

def default_error_responce(e):
    return {
        'status': 'error',
        'reason': str(e)
    }

def user_not_found_responce(e):
    return ({
        'status': 'error',
        'reason': str(e)
    }, 404)