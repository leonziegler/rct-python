'''
Created on Apr 20, 2015

@author: nkoester
'''

import abc


class TransformCommunicator(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, params):
        '''
        Constructor
        '''

    @abc.abstractmethod
    def init(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def shutdown(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def add_transform_listener(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_transform_listener(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_transforms(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def request_sync(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def print_contents(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def send_transform(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def publish_cache(self):
        raise NotImplementedError()
