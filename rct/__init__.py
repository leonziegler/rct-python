'''
Created on Apr 13, 2015

@author: nkoester
'''
# imports for availability to end users
from rct.core.Transform import Transform
from rct.util import TransformType
from rct.core.Affine3d import Affine3d

class TransformerFactory(object):
    '''
    Singlet to create a unified transformer factory
    '''
    from rct.util import Singleton
    from rct.core.TransformerConfig import TransformerConfig
    __metaclass__ = Singleton

    __core = None
    __comms = None
    __listeners = None

    def __init__(self):
        self.__comms = []
        self.__listeners = []

    def create_transform_receiver(self, listeners=[], configuration=TransformerConfig()):
        '''
        Creates an instance of the transform receiver implementation.

        :param listener: list of listeners
        :param configuration: A TransformerConfig
        :return: Instance of a TransformReceiver
        '''
        # imports
        from rct.core.TransformerTF2 import TransformerTF2
        from rct.communication.TransformCommRSB import TransformCommRSB
        from rct.util import CommunicatorType

        local_comms = []

        # deal with the listeners
        for a_listener in listeners:
            self.__listeners.append(a_listener)

        self.__core = TransformerTF2(configuration.get_cache_time())
        self.__listeners.append(self.__core)

        # Create the communication backend
        if (configuration.get_comm_type() in (CommunicatorType.AUTO, CommunicatorType.RSB)):
            local_comms.append(TransformCommRSB("read-only", self.__listeners))

        if (configuration.get_comm_type() is CommunicatorType.ROS):
            raise Exception("ROS communicator not supported :(")

        if len(local_comms) == 0:
            raise Exception("Can not generate communicator {}".format(configuration.get_comm_type()))

        # TODO: see cpp code
        local_comms[0].init(configuration)

        from rct.core.TransformReceiver import TransformReceiver
        return TransformReceiver(self.__core, local_comms[0], configuration)

    def create_transform_publisher(self, name, configuration=TransformerConfig()):
        '''
        Creates an instance of the transform publisher implementation.

        :param name: The desired name
        :param configuration: A TransformerConfig
        :return: Instance of a TransformPublisher
        '''
        # imports
        from rct.communication.TransformCommRSB import TransformCommRSB
        from rct.util import CommunicatorType
        from rct.core.TransformPublisher import TransformPublisher

        local_comms = []

        # Create the communication backend
        if (configuration.get_comm_type() in (CommunicatorType.AUTO, CommunicatorType.RSB)):
            local_comms.append(TransformCommRSB(name))

        if (configuration.get_comm_type() is CommunicatorType.ROS):
            raise Exception("ROS communicator not supported :(")

        if len(local_comms) == 0:
            raise Exception("Can not generate communicator {}".format(configuration.get_comm_type()))

        # TODO: see cpp code
        local_comms[0].init(configuration);
        return TransformPublisher(local_comms[0], configuration)

if __name__ == '__main__':
    print "import this lib to use rct..."
