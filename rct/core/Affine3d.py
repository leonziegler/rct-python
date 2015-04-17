'''
Created on Apr 16, 2015

@author: nkoester
'''
from rct.util import pretty_float


class Affine3d(object):

    '''
    Simple container datatype to hold the three components to construct an
    Affine 3d representation.
    '''

    # TODO: integrate with numpy in order to allow methods as used in C++ Eigen

    def __init__(self, translation, rotation, scale):
        '''
        Constructor
        '''
        self.__translation = translation
        self.__rotation = rotation
        self.__scale = scale

    def get_translation(self):
        return self.__translation

    def set_translation(self, value):
        self.__translation = value

    translation = property(get_translation, set_translation)

    def get_rotation(self):
        return self.__rotation

    def set_rotation(self, value):
        self.__rotation = value

    rotation = property(get_rotation, set_rotation)

    def set_scale(self, value):
        self.__scale = value

    def get_scale(self):
        return self.__scale

    scale = property(get_scale, set_scale)

    def __str__(self, *args, **kwargs):
        return "{}{}{}".format(map(pretty_float, self.translation), map(pretty_float, self.rotation), map(pretty_float, self.scale))
