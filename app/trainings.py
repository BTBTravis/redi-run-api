import os
import time
import json
from pprint import pprint
import requests

from app.cache import set_with_ttl, get_with_cache

def get_trainings():
    """Get trainings from cache falling back to api call"""
    return json.loads(get_with_cache('Trainings', _get_remote('Trainings')))

def get_training_types():
    """Get training types from cache falling back to api call"""
    return json.loads(get_with_cache('Types', _get_remote('Types')))

def get_plans():
    """Get plans from cache falling back to api call"""
    return json.loads(get_with_cache('Plans', _get_remote('Plans')))

def _get_remote(remote_key):
    """Fn to get data from airtable"""
    return lambda: _get_all_airtable(remote_key)

def _get_all_airtable(air_table_key):
    """Get some data from airtable trainings base"""
    enities = []
    offset_code = ''
    more_data = True
    while more_data:
        api_key = os.getenv('AIR_TABLE_API_KEY')
        url = f'https://api.airtable.com/v0/appaquLxmjLBX7XUc/{air_table_key}'
        params = {
            'view': 'full'
        }
        if (offset_code is not ''):
            params['offset'] = offset_code
        headers = {
            'authorization': f'Bearer {api_key}'
        }
        res = requests.request("GET", url, headers=headers, params=params)
        if (not (res.status_code >= 200 and res.status_code < 400)):
            pprint({
                'status_code': res.status_code
            })
            raise Exception('failed to get air table data')
        data = res.json()
        enities.extend(data['records'])
        if 'offset' in data:
            offset_code = data['offset']
            time.sleep(0.25) # sleep to avoid going ovre rate limit 
        else:
            more_data = False

    enities_json = json.dumps(enities)
    set_with_ttl(air_table_key, enities_json, 60)
    return enities_json