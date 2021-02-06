import logging
from logging import Logger
import sys


def make_logger(name: str='Default Logger', type: str='console', file_path: str='./example.log', mongodb_uri: str='mongodb://127.0.0.1:27017', kafka_bootstrap_servers: str=['localhost:9092'], kafka_topic: str='logs') -> Logger:
    """
    Creates a logger instance
    :param str name: The name of the logger
    :param str type: The type of logger (console, mongo, file, kafka)
    :param str file_path: Location of the log file
    :param str mongodb_uri: URI to the MongoDB database
    :param str kafka_bootstrap_servers: Kafka server
    :param str kafka_topic: Kafka topic
    :return: The logger object
    :rtype: Logger
    :raises Exception: if the type is invalid
    """
    objLogger: Logger = logging.getLogger(name)
    objLogger.setLevel(logging.DEBUG)

    if type != 'console':
        objLogger.handlers = []
        objLogger.propagate = False

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    lh = None

    if type == 'console':
        lh = logging.StreamHandler()
    elif type == 'file':
        lh = logging.FileHandler(file_path)  # '/home/kafka/KafkaConsumer.log')
    elif type == 'mongo':
        # log4mongo  # Buggy
        # from log4mongo.handlers import MongoHandler
        # lh = MongoHandler(host=mongodb_uri)

        # mongolog  # Buggy
        # from mongolog.handlers import MongoHandler
        # import pymongo
        # # dbsrv_cfg = pymongo.uri_parser.parse_uri(mongodb_uri)
        # lh = MongoHandler.to(db='mongolog', collection='logs'
        #                      # host=dbsrv_cfg['nodelist'][0][0]+':'+str(dbsrv_cfg['nodelist'][0][1]),
        #                      # username=dbsrv_cfg['username'], password=dbsrv_cfg['password']
        #                      )

        # Custom handler
        # sys.path.insert(0, dir(__file__))
        from logmagic.MongoHandler import MongoHandler
        lh = MongoHandler(mongodb_uri=mongodb_uri)
    elif type == 'kafka':
        # TODO Test a pre-built handler and pass kafka_bootstrap_servers and kafka_topic
        pass
    else:
        raise Exception('Invalid type - must be console or file')

    lh.setLevel(logging.DEBUG)
    lh.setFormatter(formatter)
    objLogger.addHandler(lh)

    return objLogger

