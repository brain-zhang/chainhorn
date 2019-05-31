# -*- coding: utf-8 -*-

import logging
import logging.config


def init_logging():
    logging.config.dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                # 'stream': 'ext://flask.logging.wsgi_errors_stream',
                'stream': 'ext://sys.stderr',
                'formatter': 'default'
            },
            'pyspv': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stderr',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['wsgi', 'pyspv']
        }
    })
