import json
import os
from functools import wraps
from pprint import pprint

import requests
from flask import request, g
from six.moves.urllib.request import urlopen
from jose import jwt

from app import app
from app.cache import set_with_ttl, cache_get

# Nearly all this code was copied and refactored from https://auth0.com/docs/quickstart/backend/python/01-authorization

AUTH0_DOMAIN = 'travisshears-dev.eu.auth0.com'
API_AUDIENCE = 'https://redi.travisshears.xyz/api/run/v1'
ALGORITHMS = ["RS256"]

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


@app.errorhandler(AuthError)
def handle_auth_error(ex):
    reason = json.dumps(ex.error)
    return reason, ex.status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    # check  for auth header
    if not auth:
        raise AuthError({"code": "authorization_header_missing",
                         "description": "Authorization header is expected"}, 401)

    parts = auth.split()

    # check for bearer
    if parts[0].lower() != "bearer":
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must start with Bearer"}, 401)
    elif len(parts) == 1:
        raise AuthError({"code": "invalid_header",
                         "description": "Token not found"}, 401)
    elif len(parts) > 2:
        raise AuthError({"code": "invalid_header",
                         "description": "Authorization header must be Bearer token"}, 401)

    token = parts[1]
    return token


def requires_auth(f):
    """Determines if the Access Token is valid"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen("https://"+AUTH0_DOMAIN+"/.well-known/jwks.json")
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError:
            raise AuthError({"code": "token_headers_invalid",
                             "description": "token is invalid"}, 401)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_AUDIENCE,
                    issuer="https://"+AUTH0_DOMAIN+"/"
                )
            except jwt.ExpiredSignatureError:
                raise AuthError({"code": "token_expired",
                                 "description": "token is expired"}, 401)
            except jwt.JWTClaimsError:
                raise AuthError({"code": "invalid_claims",
                                 "description": "incorrect claims," "please check the audience and issuer"}, 401)
            except Exception:
                raise AuthError({"code": "invalid_header",
                                 "description": "Unable to parse authentication" " token."}, 401)
            g.user = payload
            return f(*args, **kwargs)
        raise AuthError({"code": "invalid_header",
                         "description": "Unable to find appropriate key"}, 401)
    return decorated

def delete_auth0_user(auth0_id):
    token = _get_auth0_token_with_cache()
    url = f'https://{AUTH0_DOMAIN}/api/v2/users/{auth0_id}'
    headers = {
        'authorization': f'Bearer {token}'
    }
    res = requests.request("DELETE", url, headers=headers)
    if (not (res.status_code >= 200 and res.status_code < 400)):
        raise Exception('failed to delete user from auth0')
    return {
        'status_code': res.status_code
    }


auth0_token_cache_key = 'auth0_token'

def _get_auth0_token_with_cache():
    cached_token = cache_get(auth0_token_cache_key)
    cached_token = cached_token.decode("utf-8") 
    if cached_token is None:
        return _get_auth0_token()
    return cached_token

def _get_auth0_token():
    url = "https://{AUTH0_DOMAIN}/oauth/token"
    payload = {
        "client_id": os.getenv('AUTH0_API_CLIENT_ID'),
        "client_secret": os.getenv('AUTH0_API_SECRET'),
        "audience": "https://{AUTH0_DOMAIN}/api/v2/",
        "grant_type": "client_credentials",
    }
    res = requests.request("POST", url, json=payload)
    data = res.json()
    token = data['access_token']
    expires_in = data['expires_in'] - 1000
    set_with_ttl(auth0_token_cache_key, token, expires_in)
    return token
