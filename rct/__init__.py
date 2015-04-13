'''
Created on Apr 13, 2015

@author: nkoester
'''

class CommunicatorType(object):
    '''
    Enum fake.
    '''
    AUTO = 1
    RSB = 2
    ROS = 3

class TransformerConfig(object):
    '''
    Configuration holder.
    '''

    __chache_time = None
    __communicator_type = None

    def __init__(self, communicator_type="RSB", chache_time=5.0):

        self.__communicator_type = getattr(CommunicatorType, communicator_type, 'RSB')
        self.__chache_time = chache_time

#         if hasattr(CommunicatorType, communicator_type):
#             self.__communicator_type = eval(CommunicatorType.communicator_type)
#
#         else:
#             raise Exception("Communicator type {} is not supported".format(communicator_type))

    def get_chache_time(self):
        return self.__cache_time


class TransformerTF2(object):

    def __init__(self):
        pass

class TransformerFactory(object):
    from rct.util import Singleton
    '''
    Singlet to create a unified transformer factory
    '''
    __metaclass__ = Singleton

    __core = None
    __comms = None
    __listeners = None

    def __init__(self):
        self.__comms = []
        self.__listeners = []

    def create_transform_receiver(self, listeners=[], config=TransformerConfig()):
        '''

        :param listener: list of listeners
        :param config:
        '''
        for a_listener in listeners:
            self.__listeners.append(a_listener)

        self.__core = TransformerTF2(config.get_cache_time())
        self.__listeners.append(self.__core)
        # TODO FINISH

    def create_transform_receivers(self, listeners, config=TransformerConfig()):
        '''

        :param listeners: array of listeners
        :param config:
        '''
        pass

    def create_transform_publisher(self, name, config=TransformerConfig()):
        '''

        :param name:
        :param config:
        '''



if __name__ == '__main__':
    print "import this lib to use rct..."
