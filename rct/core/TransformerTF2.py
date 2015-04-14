'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct.core.TransformListener import TransformListener


# TODO: ABC this class
# base class in cpp: TransformerCore
# Q: is the TransformerCore a Transform Listener?
class TransformerTF2(TransformListener):
    '''
    classdocs
    '''

    __cache_time = None

    def __init__(self, cache_time):
        '''
        Constructor
        '''
        self.__cache_time = cache_time


    def new_transform_available(self, transform, is_static):
        print "LOL i got data: {}, {}".format(transform, is_static)
