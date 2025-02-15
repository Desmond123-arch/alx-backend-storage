#!/usr/bin/env python3
""" Writing String to redis """
import uuid
import redis
from typing import Union, Callable, Optional, Any
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ Add input parameters to redis everytime its called"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.rpush(inputs, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(outputs, str(res))
        return res
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ Returns the function increments everytime the funcion is called"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method_key
    return wrapper


def replay(method: Callable) -> None:
    """ Displays the history of calls of a function"""
    method_key = method.__qualname__
    inputs, outputs = method_key + ':inputs', method_key + ':outputs'
    redis = method.__self__._redis
    method_count = redis.get(method_key).decode('utf-8')
    print(f'{method_key} was called {method_count} times:')
    IOTuple = zip(redis.lrange(inputs, 0, -1), redis.lrange(outputs, 0, -1))
    for inp, outp in list(IOTuple):
        attr, data = inp.decode("utf-8"), outp.decode("utf-8")
        print(f'{method_key}(*{attr}) -> {data}')


class Cache:
    """
    _redis: private variable  to save a redis instance
    store: method that generateds a ramdon key
    """

    def __init__(self) -> None:
        """ stores an instance of a redis client"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[int, str, bytes, float]) -> str:
        """ Stores a data in the database"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable[..., Any]] = None):
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: str) -> str:
        """ Convert to string"""
        return data.decode('utf-8')

    def get_int(self, data: int) -> int:
        """ Covert to int"""
        return int(data)
