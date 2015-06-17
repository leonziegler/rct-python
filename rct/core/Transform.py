'''
Created on Apr 13, 2015

@author: nkoester
'''
import logging

from rct.util import get_logger_by_class
from rct.core.Affine3d import Affine3d


class Transform(object):

    '''
    classdocs
    '''

    __transformation = None
    __frame_parent = None
    __frame_child = None
    __timestamp = None
    __authority = None
    __logger = None

    def __init__(self, affine3d_transform, frame_parent, frame_child, timestamp, authority=""):
        '''
        Constructor
        '''
        assert isinstance(
            affine3d_transform, Affine3d), "Transform has to be of type rct.core.Affine3d!"

        self.__transformation = affine3d_transform
        self.__frame_parent = frame_parent
        self.__frame_child = frame_child
        self.__timestamp = timestamp
        self.__authority = authority
        self.__logger = get_logger_by_class(self.__class__)

    def apply_transformation(self, a_point):
        '''
        Applies the thransformation to a given vector.
        :param a_point: vec3 or vec4
        '''
        return self.transform.apply_transformation(a_point)

    def get_transformation(self):
        return self.__transformation

    transformation = property(get_transformation, )

    def get_frame_parent(self):
        return self.__frame_parent

    frame_parent = property(get_frame_parent, )

    def get_frame_child(self):
        return self.__frame_child
    frame_child = property(get_frame_child, )

    def get_authority(self):
        return self.__authority
    authority = property(get_authority, )

    def get_timestamp(self):
        return self.__timestamp
    timestamp = property(get_authority, )

    def print_contents(self, level=logging.INFO):
        self.__logger.log(level, "authority: {}, frame_parent: {}, frame_child: {}, timestamp: {}, transform: {}".format(
            self.__authority, self.__frame_parent, self.__frame_child, self.__timestamp, self.__transformation))

    def __str__(self):
        return "authority: {},\nframe_parent: {},\nframe_child: {},\ntimestamp: {},\ntransform: {}".format(
            self.__authority, self.__frame_parent, self.__frame_child, self.__timestamp, self.__transformation)