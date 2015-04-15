'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct.core.Transform import Transform
from rct.util import TransformType

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
        Creates the chosen transform receiver implementation.
        :param listener: list of listeners
        :param configuration: A TransformerConfig
        :return: Instance of a TransformReceiver
        '''
        # imports
        from rct.core.TransformerTF2 import TransformerTF2
        from rct.communication.TransformCommRSB import TransformCommRSB
        from rct.util import CommunicatorType

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
        # imports
        from rct.communication.TransformCommRSB import TransformCommRSB
        from rct.util import CommunicatorType

        # Create the communication backend
        if (configuration.get_comm_type() in (CommunicatorType.AUTO, CommunicatorType.RSB)):
            new_comm = TransformCommRSB(name)

        if (configuration.get_comm_type() is CommunicatorType.ROS):
            raise Exception("ROS communicator not supported :(")

        if len(self.__comms) == 0:
            raise Exception("Can not generate communicator {}".format(configuration.get_comm_type()))

        # TODO: see cpp code
        new_comm.init(configuration);
        # TODO: why was this it in the cpp code? this now works ... weird!
        self.__comms.append(new_comm)

        from rct.core.TransformPublisher import TransformPublisher
        return TransformPublisher(new_comm, configuration)



if __name__ == '__main__':
    print "import this lib to use rct..."
    import time
    import rct
    import logging
    logging.basicConfig()
    a = rct.TransformerFactory()
    r = a.create_transform_receiver()
    p = a.create_transform_publisher("blubbAuth")

    t_s = rct.Transform("blub", "parentoruu", "childoruu", time.time())
    p.send_transform(t_s, rct.TransformType.STATIC)

    # t_d = rct.Transform("bla", "leParent", "leChild", time.time())
    # p.send_transform(t_d, rct.TransformType.DYNAMIC)

    # err
    # p.send_transform(rct.Transform(), rct.TransformType.STATIC)

    print "done."
