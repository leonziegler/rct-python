'''
Created on Apr 13, 2015

@author: nkoester
'''

class TransformReceiver(object):
    '''
    Interface to create Transformation receivers.
    '''
    from rct.core.TransformerConfig import TransformerConfig
    __core = None
    __comm = None
    __config = None

    def __init__(self, core, comm, config=TransformerConfig()):
        '''
        Constructor.
        '''
        self.__core = core
        self.__comm = comm
        self.__config = config

    def print_contents(self):
        self.__core.print_contents()
        self.__comm.print_contents()
        self.__config.print_contents()

    def get_config(self):
        # TODO: why not return core config here?
        return self.__config

    def get_authority_name(self):
        self.__comm.get_authority_name()

    def lookup_transform(self, target_frame, source_frame, a_time):
        '''
        Get the transform between two frames by frame ID.
        :param target_frame: (string) The frame to which data should be transformed
        :param source_frame: (string) The frame where the data originated
        :param a_time: The time at which the value of the transform is desired. (0 will get the latest)
        :return: The transform between the frames
        '''
        # TODO: implement
        return self.__core.lookup_transform(target_frame, source_frame, a_time)

    def lookup_transform_with_times(self, target_frame, target_time, source_frame, source_time, fixed_frame):
        '''
        Get the transform between two frames by frame ID assuming fixed frame.
        :param target_frame: The frame to which data should be transformed
        :param target_time: The time to which the data should be transformed. (0 will get the latest)
        :param source_frame: The frame where the data originated
        :param source_time: The time at which the source_frame should be evaluated. (0 will get the latest)
        :param fixed_frame: The frame in which to assume the transform is constant in time.
        :return: The transform between the frames
        '''
        return self.__core.lookup_transform_with_times(target_frame, target_time, source_frame, source_time, fixed_frame)

    def request_transform(self, target_frame, source_frame, time):
        '''
        Request the transform between two frames by frame ID.
        :param target_frame: The frame to which data should be transformed
        :param source_frame: The frame where the data originated
        :param time: The time at which the value of the transform is desired. (0 will get the latest)
        :return: A future object representing the request status and transform between the frames
        '''
        return self.__core.request_transform(target_frame, source_frame, time)

    def can_transform(self, target_frame, source_frame, time, error_msg):
        '''
        Test if a transform is possible.
        :param target_frame: The frame into which to transform
        :param source_frame: The time into which to transform
        :param time: The time at which to transform
        :param error_msg: A pointer to a string which will be filled with why the transform failed, if not NULL
        :return: True if the transform is possible, false otherwise
        '''
        return self.__core.can_transform(target_frame, source_frame, time, error_msg)

    def can_transform_with_times(self, target_frame, target_time, source_frame, source_time, fixed_frame, error_msg):
        '''
        Test if a transform is possible
        :param target_frame: The frame into which to transform
        :param target_time: The time into which to transform
        :param source_frame: The time into which to transform
        :param source_time: The time from which to transform
        :param fixed_frame: The frame in which to treat the transform as constant in time
        :param error_msg: A pointer to a string which will be filled with why the transform failed, if not NULL
        :return: True if the transform is possible, false otherwise
        '''
        return self.__core.can_transform_with_times(target_frame, target_time, source_frame, source_time, fixed_frame, error_msg);

    def get_core(self):
        return self.__core

    def shutdown(self):
        self.__comm.shutdown()
