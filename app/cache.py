import os
import redis

cache_prefix='redi_run_api_'
redis_url = os.getenv('REDIS_HOST')
conn = redis.from_url(redis_url)

def set_with_ttl(key, val, ttl):
    prefixed_key = f'{cache_prefix}{key}'
    conn.set(prefixed_key, val)
    conn.expire(prefixed_key, ttl)

def cache_get(key): 
    prefixed_key = f'{cache_prefix}{key}'
    return conn.get(prefixed_key)
