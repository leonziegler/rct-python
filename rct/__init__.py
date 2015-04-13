'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct.communication.TransformCommRSB import TransformCommRSB

class CommunicatorType(object):
    '''
    Enum fake.
    '''
    AUTO = "AUTO"
    RSB = "RSB"
    ROS = "ROS"

class TransformerConfig(object):
    '''
    Configuration holder.
    '''

    __cache_time = None
    __communicator_type = None

    def __init__(self, communicator_type="RSB", chache_time=5.0):

        self.__communicator_type = getattr(CommunicatorType, communicator_type, 'RSB')
        self.__cache_time = chache_time

#         if hasattr(CommunicatorType, communicator_type):
#             self.__communicator_type = eval(CommunicatorType.communicator_type)
#
#         else:
#             raise Exception("Communicator type {} is not supported".format(communicator_type))

    def get_cache_time(self):
        return self.__cache_time

    def print_contents(self):
        print "comm_type: {}, cache_time: {}".format(self.__communicator_type, self.__cache_time)

    def get_comm_type(self):
        return self.__communicator_type

class TransformerTF2(object):

    __cache_time = None

    def __init__(self, cache_time):
        self.__cache_time = cache_time

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

    def create_transform_receiver(self, listeners=[], configuration=TransformerConfig()):
        '''
        Creates the chosen transform receiver implementation.
        :param listener: list of listeners
        :param configuration: A TransformerConfig
        :return: Instance of a TransformReceiver
        '''

        # deal with the listeners
        for a_listener in listeners:
            self.__listeners.append(a_listener)

        self.__core = TransformerTF2(configuration.get_cache_time())
        self.__listeners.append(self.__core)


        # Create the communication backend
        if (configuration.get_comm_type() in (CommunicatorType.AUTO, CommunicatorType.RSB)):
            self.__comms.append(TransformCommRSB("read-only", self.__listeners))

        if (configuration.get_comm_type() is CommunicatorType.ROS):
            raise Exception("ROS communicator not supported :(")

        if len(self.__comms) == 0:
            raise Exception("Can not generate communicator {}".format(configuration.get_comm_type()))

        # TODO: see cpp code
        self.__comms[0].init(configuration)

        from rct.core.TransformReceiver import TransformReceiver
        return TransformReceiver(self.__core, self.__comms[0], configuration)



    def create_transform_publisher(self, name, configuration=TransformerConfig()):
        '''
        Creates the chosen transform publisher implementation.
        :param name: The desired name
        :param configuration: A TransformerConfig
        :return: Instance of a TransformPublisher
        '''

        # Create the communication backend
        if (configuration.get_comm_type() in (CommunicatorType.AUTO, CommunicatorType.RSB)):
            self.__comms.append(TransformCommRSB(name))

        if (configuration.get_comm_type() is CommunicatorType.ROS):
            raise Exception("ROS communicator not supported :(")

        if len(self.__comms) == 0:
            raise Exception("Can not generate communicator {}".format(configuration.get_comm_type()))

        # TODO: see cpp code
        self.__comms[0].init(configuration);

        from rct.core.TransformPublisher import TransformPublisher
        return TransformPublisher(self.__comms[0], configuration)



if __name__ == '__main__':
    print "import this lib to use rct..."
