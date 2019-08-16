# -*- coding: utf-8 -*-

import logging
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
