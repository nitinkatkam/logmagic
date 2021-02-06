import logging
from typing import NoReturn

from pymongo import MongoClient
from pymongo.errors import ConfigurationError
from pymongo import Collection
from pymongo import Database
from datetime import datetime
from socket import gethostname
from time import tzname
from platform import platform
from getpass import getuser
from os import getpid, getcwd  #, getuid  # GetUid doesn't exist on Windows


class MongoHandler(logging.Handler):
    """
    Handler for logging to MongoDB
    """

    def __init__(
            self,
            level: int = logging.NOTSET,
            collection: str = 'log',
            mongodb_uri: str = 'mongodb://127.0.0.1:27017/test'
    ):
        """
        Constructor
        :param str level: Log level (use the constants from the logging package, or specify the int values)
        :param str collection: Name of the collection (table) to store the log messages in
        :param str mongodb_uri: URI to the MongoDB database
        """
        logging.Handler.__init__(self, level)
        client: MongoClient = MongoClient(mongodb_uri)
        try:
            db: Database = client.get_default_database()
        except ConfigurationError as cfg_err:
            # noinspection PyPep8Naming
            CONST_NO_DEFAULT_IN_URI_ERRMSG: str = 'No default database name defined or provided.'
            if cfg_err.args[0] == CONST_NO_DEFAULT_IN_URI_ERRMSG:
                db = client.test
            else:
                raise cfg_err
        self.collection: Collection = db[collection]

    def emit(self, obj_log_msg: object) -> NoReturn:
        self.collection.save(
            {
                'message': obj_log_msg.msg,
                'loggerInfo': {
                    'loggerName': obj_log_msg.name,
                    'logLevel': obj_log_msg.levelname,
                    'loggedAt': datetime.utcnow(),
                },
                'host': {
                    'hostName': gethostname(),
                    'localTimeZone': tzname,
                    'platform': platform(),
                },
                'location': {
                    'module': obj_log_msg.module,
                    'path': obj_log_msg.pathname,
                    'file': obj_log_msg.filename,
                    'funcName': obj_log_msg.funcName,
                    'lineNo': obj_log_msg.lineno,
                },
                'processInfo': {
                    'username': getuser(),
                    #'uid': getuid(),  # TODO Not available on Windows
                    'processId': getpid(),
                    'workingDirectory': getcwd()
                },
            }
        )
