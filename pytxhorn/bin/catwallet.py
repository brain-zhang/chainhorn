# -*- coding: utf-8 -*-

import include
import settings
import logging
import pprint
from contrib.node import get_spv_node

logger = logging.getLogger('default')

if __name__ == '__main__':
    spv = get_spv_node(settings, need_load_blocks=False)
    wallet = spv.wallet
    wallet_temp_info = wallet.get_temp_collections()

    pp = pprint.PrettyPrinter(indent=4)
    wallet_temp_info = "\r\n{}".format(pp.pformat(wallet_temp_info))
    logger.info(wallet_temp_info)
