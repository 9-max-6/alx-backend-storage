#!/usr/bin/env python3
"""Module: class Cache
"""
import redis
import uuid
from typing import Union, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """A decoratpr that implements a counting technique to determine
    the number of types a function has been called
    """
    @wraps(method)
    def wrapper(self, data: Union[str, bytes, int, float]):
        """Wrapper function increment the value of key in redis
        """
        self._redis.incr(method.__qualname__)
        return method(self, data)
    return wrapper

class Cache():
    """A class to initialize a redis cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store method that takes a data argument
        and returns a string.
        """
        rand_key = uuid.uuid4()
        if self._redis.mset({str(rand_key): data}):
            return str(rand_key)
    def get(self, key: str, fn: Callable = None) -> Union[str, float, int, bytes]:
        """This callable will be used to convert the data
        back to the desired format.
        """
        value = self._redis.get(key)
        if fn:
            return fn(value)
        else:
            return value

    def get_str(self, key: str) -> str:
        """returns a string value from Redis data storage.
        """
        return self.get(key, lambda x: x.decode("utf-8"))

    def get_int(self, key: str) -> int:
        """returns a integer value from Redis data storage.
        """
        return self.get(key, lambda x: int(x))
