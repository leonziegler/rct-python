'''
Created on Apr 13, 2015

@author: nkoester
'''

class TransformerConfig(object):
    '''
    Configuration holder.
    '''

    __cache_time = None
    __communicator_type = None

    def __init__(self, communicator_type="RSB", chache_time=5.0):
        # imports
        from rct.util import CommunicatorType

        self.__communicator_type = getattr(CommunicatorType, communicator_type, 'RSB')
        self.__cache_time = chache_time

    def get_cache_time(self):
        return self.__cache_time

    def print_contents(self):
        print "comm_type: {}, cache_time: {}".format(self.__communicator_type, self.__cache_time)

    def get_comm_type(self):
        return self.__communicator_type
