'''
TWINT - Twitter Intelligence Tool (formerly known as Tweep).

See wiki on Github for in-depth details.
<<<<<<< HEAD
https://github.com/haccer/twint/wiki
=======
https://github.com/twintproject/twint/wiki
>>>>>>> master

Licensed under MIT License
Copyright (c) 2018 Cody Zacharias
'''
<<<<<<< HEAD
from .config import Config
from . import run

#import logging
#logger = logging.getLogger()
#handler = logging.FileHandler('twint.log')
#formatter = logging.Formatter(
#        '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
#handler.setFormatter(formatter)
#logger.addHandler(handler)
#logger.setLevel(logging.DEBUG)
=======
import logging, os

from .config import Config
from .__version__ import __version__
from . import run

_levels = {
    'info': logging.INFO,
    'debug': logging.DEBUG
}

_level = os.getenv('TWINT_DEBUG', 'info')
_logLevel = _levels[_level]

if _level == "debug":
    logger = logging.getLogger()
    _output_fn = 'twint.log'
    logger.setLevel(_logLevel)
    formatter = logging.Formatter('%(levelname)s:%(asctime)s:%(name)s:%(message)s')
    fileHandler = logging.FileHandler(_output_fn)
    fileHandler.setLevel(_logLevel)
    fileHandler.setFormatter(formatter)
    logger.addHandler(fileHandler)
>>>>>>> master
