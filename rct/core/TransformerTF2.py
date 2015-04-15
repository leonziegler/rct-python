'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct.core.TransformListener import TransformListener
from rct.util import get_logger_by_class


# TODO: ABC this class
# base class in cpp: TransformerCore
class TransformerTF2(TransformListener):
    '''
    classdocs
    '''

    __cache_time = None
    __logger = None

    def __init__(self, cache_time):
        '''
        Constructor
        '''
        self.__cache_time = cache_time
        self.__logger = get_logger_by_class(self.__class__)

    def new_transform_available(self, transform, is_static):
        self.__logger.info("LOL i got data: {}, {}".format(transform, is_static))
