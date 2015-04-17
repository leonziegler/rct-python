'''
Created on Apr 13, 2015

@author: nkoester
'''
import logging


class TransformPublisher(object):

    '''
    Interface to create Transformation publishers.
    '''

    from rct.core.TransformerConfig import TransformerConfig

    __comm = None
    __config = None

    def __init__(self, comm, config=TransformerConfig()):
        '''
        Constructor
        '''
        self.__comm = comm
        self.__config = config

    def print_contents(self, log_level=logging.INFO):
        self.__comm.print_contents(level=log_level)
        self.__config.print_contents(level=log_level)

    def get_config(self):
        return self.__comm.get_config()

    def get_authority_name(self):
        self.__comm.get_authority_name()

    def send_transform(self, transform, transform_type):
        '''
        Add transform information to the rct data structure.
        :param transform: The transform to store
        :param transform_type: The type of transform
        '''
        return self.__comm.send_transform(transform, transform_type)

    def send_transforms(self, transforms, transform_type):
        '''
        Add transform information to the rct data structure
        :param transforms: A list of transformations
        :param transform_type: The type of transform
        '''
        return self.__comm.send_transforms(transforms, transform_type)

    def shutdown(self):
        self.__comm.shutdown()
