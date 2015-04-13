'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct import TransformerConfig

class TransformPublisher(object):
    '''
    Interface to create Transformation publishers.
    '''
    __comm = None
    __config = None

    def __init__(self, comm, config=TransformerConfig()):
        '''
        Constructor
        '''
        self.__comm = comm
        self.__config = config

    def print_contents(self):
        self.__comm.print_contents()
        self.__config.print_contents()

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
