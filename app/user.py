import json
from pprint import pprint

from mongoengine import *

class _User(Document):
    auth0_id = StringField(required=True)
    age = IntField()
    resting_heart_rate = IntField()

class User():
    def __init__(self, passed_auth0_id):
        # print(f'passed_auth0_id:{passed_auth0_id}')
        possible_users = _User.objects(auth0_id=passed_auth0_id)
        # print(f'possible_users len:{len(possible_users) > 0}')
        if len(possible_users) > 0:
            self._user = possible_users[0]
        else:
            self._user = _User(auth0_id=passed_auth0_id)
            self._user.save()

    def update(self, fields):
        """given a list of tups update the keys on the user"""
        for field in fields:
            self._user[field] = fields[field]
        self._user.save()
    
    def delete(self):
        """delete underlying user document"""
        self._user.delete()

    def dump(self):
        """Return a object that can be json dumped and is clean of _id"""
        json_user = self._user.to_json()
        user = json.loads(json_user)
        del user["_id"]
        return user
