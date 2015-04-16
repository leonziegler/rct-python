'''
Created on Apr 13, 2015

@author: nkoester
'''
import logging


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

    def print_contents(self, log_level=logging.INFO):
        self.__core.print_contents(level=log_level)
        self.__comm.print_contents(level=log_level)
        self.__config.print_contents(level=log_level)

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

    def lookup_transform_full(self, target_frame, target_time, source_frame, source_time, fixed_frame):
        '''
        Get the transform between two frames by frame ID assuming fixed frame.
        :param target_frame: The frame to which data should be transformed
        :param target_time: The time to which the data should be transformed. (0 will get the latest)
        :param source_frame: The frame where the data originated
        :param source_time: The time at which the source_frame should be evaluated. (0 will get the latest)
        :param fixed_frame: The frame in which to assume the transform is constant in time.
        :return: The transform between the frames
        '''
        return self.__core.lookup_transform_full(target_frame, target_time, source_frame, source_time, fixed_frame)

    def can_transform(self, target_frame, source_frame, time, error_msg):
        '''
        Test if a transform is possible.
        :param target_frame: The frame into which to transform
        :param source_frame: The time into which to transform
        :param time: The time at which to transform
        :return: True if the transform is possible, false otherwise
        '''
        return self.__core.can_transform(target_frame, source_frame, time, error_msg)

    def can_transform_full(self, target_frame, target_time, source_frame, source_time, fixed_frame, error_msg):
        '''
        Test if a transform is possible
        :param target_frame: The frame into which to transform
        :param target_time: The time into which to transform
        :param source_frame: The time into which to transform
        :param source_time: The time from which to transform
        :param fixed_frame: The frame in which to treat the transform as constant in time
        :return: True if the transform is possible, false otherwise
        '''
        return self.__core.can_transform_with_times(target_frame, target_time, source_frame, source_time, fixed_frame, error_msg);

    def all_frames_as_string(self):
        return self.__core.all_frames_as_string()

    def all_frames_as_YAML(self):
        return self.__core.all_frames_as_YAML()

    def clear(self):
        self.__core.clear()

    def get_core(self):
        return self.__core

    def shutdown(self):
        self.__comm.shutdown()
