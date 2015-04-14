'''
Created on Apr 13, 2015

@author: nkoester
'''

# TODO: ABC this class
# base class in cpp: TransformerCore
# Q: is the TransformerCore a Transform Listener?

class TransformerTF2(object):
    '''
    classdocs
    '''

    __cache_time = None

    def __init__(self, cache_time):
        '''
        Constructor
        '''
        self.__cache_time = cache_time
