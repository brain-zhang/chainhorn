# -*- coding: utf-8 -*-

import dbm
from shelve import Shelf


class DbfilenameShelfX(Shelf):
    """Shelf implementation using the "dbm" generic dbm interface.
    This is initialized with the filename for the dbm database.
    See the module's __doc__ string for an overview of the interface.
    """

    def __init__(self, filename, flag='c', protocol=None, writeback=False):
        Shelf.__init__(self, dbm.ndbm.open(filename, flag), protocol, writeback)


def open(filename, flag='c', protocol=None, writeback=False):
    """Open a persistent dictionary for reading and writing.
    The filename parameter is the base filename for the underlying
    database.  As a side-effect, an extension may be added to the
    filename and more than one file may be created.  The optional flag
    parameter has the same interpretation as the flag parameter of
    dbm.open(). The optional protocol parameter specifies the
    version of the pickle protocol.
    See the module's __doc__ string for an overview of the interface.
    """

    return DbfilenameShelfX(filename, flag, protocol, writeback)
