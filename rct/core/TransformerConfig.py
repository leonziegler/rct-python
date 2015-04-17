'''
Created on Apr 13, 2015

@author: nkoester
'''
import logging

from rct.util import get_logger_by_class
from rct.util import CommunicatorType


class TransformerConfig(object):

    '''
    Configuration holder.
    '''

    __cache_time = None
    __communicator_type = None
    __logger = None

    def __init__(self, communicator_type="RSB", chache_time=5.0):
        # imports

        self.__communicator_type = getattr(CommunicatorType, communicator_type, 'RSB')
        self.__cache_time = chache_time
        self.__logger = get_logger_by_class(self.__class__)

    def get_cache_time(self):
        return self.__cache_time

    def print_contents(self, level=logging.INFO):
        self.__logger.log(level, "comm_type: {}, cache_time: {}".format(self.__communicator_type, self.__cache_time))

    def get_comm_type(self):
        return self.__communicator_type
