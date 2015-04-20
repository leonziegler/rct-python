'''
Created on Apr 13, 2015

@author: nkoester
'''
import abc


class TransformListener(object):

    '''
    Listener MetaClass for new Transformations.
    '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        '''
        Constructor.
        '''

    @abc.abstractmethod
    def new_transform_available(self, transform, is_static):
        '''
        Handles newly available transformation
        :param transform: New transformation
        :param is_static: true if static, false otherwise
        '''
        raise NotImplementedError()
