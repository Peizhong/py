import functools
import time
import uuid

from .config import query_config
from .database import MyMySQL, MyRedis


def clock(func):
    @functools.wraps(func)
    def clocked(*args, **kwargs):
        t0 = time.time()
        res = func(*args, **kwargs)
        arglist = []
        if args:
            pass
            #arglist.append(', '.join(repr(s) for s in args))
        if kwargs:
            pass
            #paris = ['%s=%r' % (k, w) for k, w in sorted(kwargs.items())]
            # arglist.append(','.join(paris))
        elapsed = time.time()-t0
        print('%s(%s): %r' % (func.__name__, arglist, elapsed))
        return res
    return clocked


def new_uuid():
    return uuid.uuid4().hex
