# -*- coding: utf-8 -*-

import logging
import logging.config

from . import include
from settings import LOGGING_LEVEL


def init_logging():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
                'formatter': 'default'
            }
        },
        'loggers': {
            'default': {
                'handlers': ['console'],
                'propagate': 0,
                'level': LOGGING_LEVEL,
            },
            'ohter': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        },
        'root': {
            'level': LOGGING_LEVEL,
            'handlers': ['console']
        }
    })
