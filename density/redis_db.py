import redis
import json


redis_client = redis.Redis(host='localhost', port=6379, db=0)


def set_redis(name, value, **kwargs):
    if isinstance(value, (list, dict)):
        js_value = json.dumps(value)
        redis_client.set(name=name, value=js_value, **kwargs)
    else:
        redis_client.set(name=name, value=value, **kwargs)


def get_redis(name):
    try:
        volume = redis_client.get(name).decode('utf-8')

    except:
        volume = False

    return volume