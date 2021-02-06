# LogMagic

## Description

LogMagic is a set of helper functions and log handlers around Python's built-in logging framework.

## Example

```
from logmagic.loggerutil import make_logger

logger = make_logger(name='MegaLogger', type='mongo', mongodb_uri='mongodb://user:passwd@127.0.0.1:27017/logdb?authSource=admin')
logger.debug('It is in the database')

logger = make_logger(name='SuperLogger', type='file', file_path='app.log')
logger.debug('It is in the file')

logger = make_logger(name='HyperLogger')
logger.debug('It is on the console')
```