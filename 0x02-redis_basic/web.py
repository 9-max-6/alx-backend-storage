#!/usr/bin/env python3
"""Module: a cacher implemented using redis
"""
import redis
import requests
from typing import Callable
from functools import wraps


class Cache():
    """ class to encapsulate the redis connection"""
    def __init__(self, *args, **kwargs):
        """init"""
        self._object = redis.Redis()


redis_ = Cache()


def cacher(method: Callable) -> Callable:
    """a function to implement the caching"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """ the wrapper that adds functionality and calls the
        decorated function """
        redis_._object.incr("count:{url}")
        cache_key = method.__qualname__ + ":cache"
        cached_result = redis_._object.get(cache_key)

        if cached_result:
            return cached_result.decode('utf-8')
        else:
            result = method(*args, **kwargs)
            redis_._object.setex(cached_result, 10, str(result))
            return result
    return wrapper


@cacher
def get_page(url: str) -> str:
    """a function to fetch from a url using the requests module
    """
    return requests.get(url)
