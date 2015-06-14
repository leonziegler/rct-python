'''
Created on Apr 16, 2015

@author: nkoester
'''

from rct.util import pretty_float
from pyrr import Matrix44, Quaternion, Vector3
import math
import numpy as np


class Affine3d(object):

    '''
    Simple container datatype to hold the three components to construct an
    Affine 3d representation.
    '''

    def __init__(self, translation, rotation_quaternion, scale):
        '''
        Constructor
        '''
        assert isinstance(rotation_quaternion, Quaternion), "rotation_quaternion needs to be of type pyrr.Quaternion"
        assert isinstance(translation, Vector3), "translation needs to be of type pyrr.Vector3"
        assert isinstance(scale, Vector3), "scale needs to be of type pyrr.Vector3"

        self.__translation = translation
        self.__rotation_quaternion = rotation_quaternion
        self.__scale = scale

    def get_translation(self):
        return self.__translation

    def set_translation(self, value):
        self.__translation = value

    translation = property(get_translation, set_translation)

    def get_rotation_quaternion(self):
        return self.__rotation_quaternion

    def set_rotation_quaternion(self, value):
        self.__rotation_quaternion = value

    rotation_quaternion = property(get_rotation_quaternion, set_rotation_quaternion)

    def set_scale(self, value):
        self.__scale = value

    def get_scale(self):
        return self.__scale

    scale = property(get_scale, set_scale)

    def get_rotation_matrix(self):
        return Matrix44.from_quaternion(self.__rotation_quaternion)

    def get_rotation_YPR(self):
        yawOut = math.atan2(self.__transform[1][0], self.__transform[0][0])
        pitchOut = math.asin(-self.__transform[2][0])
        rollOut = math.atan2(self.__transform[2][1], self.__transform[2][2])

        # on pitch = +/-HalfPI
        if abs(pitchOut) == (np.pi / 2.0):
            if yawOut > 0:
                yawOut -= np.pi
            else:
                yawOut += np.pi
            if pitchOut > 0:
                pitchOut -= np.pi
            else:
                pitchOut += np.pi
        return [a / np.pi * 180 for a in (yawOut, pitchOut, rollOut)]

    def get_translation_matrix(self):
        return Matrix44.from_translation(self.__translation)

    def get_transformation_matrix(self):
        return Matrix44.from_translation(self.__translation) * self.__rotation_quaternion

    def __str__(self, *args, **kwargs):
        x = self.get_transformation_matrix()
        pretty_matrix = " ; ".join(map(str, [map(pretty_float, col) for col in [a_col.tolist() for a_col in [x.r1, x.r2, x.r3, x.r4]]])).replace("'", "").replace("[", "").replace("]", "")
        return "{} | {} | {}".format(map(pretty_float, self.translation), pretty_matrix, map(pretty_float, self.scale))
