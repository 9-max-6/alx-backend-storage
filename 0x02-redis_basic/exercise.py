#!/usr/bin/env python3
"""Module: class Cache
"""
import redis
import uuid
from typing import Union, Callable, Any
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """A decoratpr that implements a counting technique to determine
    the number of types a function has been called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function increment the value of key in redis
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """A function to store the calls and their inputs
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """The function to modify then call the original function
        """
        input_key = method.__qualname__ + ":inputs"
        output_key = method.__qualname__ + ":outputs"
        self._redis.rpush(input_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


def replay(method: Callable) -> None:
    """A function to replay inputs and outputs
    """
    redis_object = method.__self__._redis

    method_name = method.__qualname__
    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"

    if isinstance(redis_object, redis.Redis):
        list_inputs = redis_object.lrange(input_key, 0, -1)
        list_outputs = redis_object.lrange(output_key, 0, -1)
        num_calls = int(redis_object.get(method_name))
    zipped_calls = zip(list_inputs, list_outputs)

    calling_card = f"{method_name} was called {num_calls} times"
    print(calling_card)

    for call in zipped_calls:
        decoded_input = call[0].decode("utf-8")
        decoded_output = call[1].decode("utf-8")
        output = f"{method_name}(*{decoded_input}) -> {decoded_output}"
        print(output)


class Cache():
    """A class to initialize a redis cache"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ store method that takes a data argument
        and returns a string.
        """
        rand_key = uuid.uuid4()
        if self._redis.mset({str(rand_key): data}):
            return str(rand_key)

    def get(
            self,
            key: str,
            fn: Callable = None
            ) -> Union[str, float, int, bytes]:
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
