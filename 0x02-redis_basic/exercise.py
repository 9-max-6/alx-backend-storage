#!/usr/bin/env python3
"""Module: class Cache
"""
import redis
import uuid
from typing import Union


class Cache():
    """A class to initialize a redis cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()
    
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store method that takes a data argument
        and returns a string.
        """
        rand_key = uuid.uuid4()
        if self._redis.mset({rand_key: data}):
            return rand_key
