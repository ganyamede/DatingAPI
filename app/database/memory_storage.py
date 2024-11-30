from redis import Redis

r = Redis(host='localhost', port=6379, db=0)

def add_to_set(uid, values):
    print(uid, values)
    r.sadd(uid, values)
    r.expire(uid, 86400)  # Устанавливаем TTL 24 часа

def check_value_in_set(uid, value):
    return r.sismember(uid, value)

def remove_from_set(uid, value):
    r.srem(uid, value)