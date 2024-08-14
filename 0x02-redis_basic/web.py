#!/usr/bin/env python3
"""Module: a cacher implemented using redis
"""
import redis
import requests
from typing import Callable, Any
from functools import wraps


redis_connection = redis.Redis()


def cacher(method: Callable) -> Callable:
    """a function to implement the caching"""
    @wraps(method)
    def wrapper(*args, **kwargs) -> str:
        """ the wrapper that adds functionality and calls the
        decorated function """
        count_name = f"count:{args[0]}"
        redis_connection.incr(count_name)
        cache_key = method.__qualname__ + ":cache"
        cached_result = redis_connection.get(cache_key)
        print(cached_result)
        if cached_result:
            return cached_result.decode('utf-8')

        else:
            result = method(*args, **kwargs)
            if result:
                redis_connection.set(count_name, 0)
                redis_connection.setex(cache_key, 10, result.text)
                return result
    return wrapper


@cacher
def get_page(url: str) -> str:
    """a function to fetch from a url using the requests module
    """
    return requests.get(url).text
