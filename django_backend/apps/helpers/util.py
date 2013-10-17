# -*- coding: utf-8 -*-
import logging, logging.handlers
from locale import setlocale, LC_ALL, LC_TIME
#setlocale(LC_TIME, '')

class EncodingFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt=None, encoding=None):
        logging.Formatter.__init__(self, fmt, datefmt)
        self.encoding = encoding

    def format(self, record):
        result = logging.Formatter.format(self, record)
        if isinstance(result, str):
            result = result.decode('utf8', 'replace')
        return result