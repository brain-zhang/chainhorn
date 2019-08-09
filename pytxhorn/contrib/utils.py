# -*- coding: utf-8 -*-

import logging
import threading
import time
import traceback

logger = logging.getLogger('default')


def exception_printer(f):
    def f2(*args, **kwargs):
        nonlocal f
        try:
            return f(*args, **kwargs)
        except Exception:
            logger.info(traceback.format_exc())
            return traceback.format_exc()
    f2.__name__ = f.__name__
    return f2


class FuncThreadClass(threading.Thread):
    """custom func and args"""

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.name = name
        self.func = func
        self.args = args

    def run(self):
        self.func(*self.args)
        time.sleep(1)
