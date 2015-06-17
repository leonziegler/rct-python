'''
Created on Apr 16, 2015

@author: nkoester
'''

from rct.util import pretty_float
from pyrr import Matrix33, Matrix44, Quaternion, Vector3, Vector4
import math
import numpy as np


class Affine3d(object):

    '''
    Simple container datatype to hold the three components to construct an
    Affine 3d representation.
    '''

    def __init__(self, translation, rotation, scale):
        '''
        Constructor
        '''
        assert isinstance(rotation, Quaternion), "rotation needs to be of type pyrr.Quaternion"
        assert isinstance(translation, Vector4), "translation needs to be of type pyrr.Vector4"
        assert isinstance(scale, Vector4), "scale needs to be of type pyrr.Vector4"

        self.__translation = translation
        self.__rotation_quaternion = rotation
        self.__scale = scale

    def apply_transformation(self, a_point):
        '''
        Applies the transformation to a given point (vec4 or vec3).
        '''
        assert isinstance(a_point, Vector4) or isinstance(a_point, Vector3)
        if isinstance(a_point, Vector4):
            return self.__apply_transformation_vec4(a_point)
        elif isinstance(a_point, Vector3):
            return self.__apply_transformation_vec3(a_point)

    def __apply_transformation_vec4(self, a_point):
        '''
        Applies the transformation to a given Verctor4.
        :param a_point: Vector4
        '''
        return (Matrix44.from_quaternion(self.__rotation_quaternion).T * a_point) + self.__translation

    def __apply_transformation_vec3(self, a_point):
        '''
        Applies the transformation to a given Verctor3.
        :param a_point: Vector3
        '''
        return (Matrix33.from_quaternion(self.__rotation_quaternion).T * a_point) + Vector3.from_vector4(self.__translation)[0]

    def __get_translation(self):
        return self.__translation

    def __set_translation(self, value):
        self.__translation = value

    translation = property(__get_translation, __set_translation)

    def __get_rotation_quaternion(self):
        return self.__rotation_quaternion

    def __set_rotation_quaternion(self, value):
        self.__rotation_quaternion = value

    rotation_quaternion = property(__get_rotation_quaternion, __set_rotation_quaternion)

    def __set_scale(self, value):
        self.__scale = value

    def __get_scale(self):
        return self.__scale

    scale = property(__get_scale, __set_scale)

    def __get_rotation_matrix(self):
        return Matrix44.from_quaternion(self.__rotation_quaternion)

    rotation_matrix = property(__get_rotation_matrix,)

    def __get_rotation_YPR(self):
        transformation_matrix = self.transformation_matrix
        yawOut = math.atan2(transformation_matrix[1][0], transformation_matrix[0][0])
        pitchOut = math.asin(-transformation_matrix[2][0])
        rollOut = math.atan2(transformation_matrix[2][1], transformation_matrix[2][2])

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

    yrp = property(__get_rotation_YPR)

    def __get_transformation_matrix(self):
        '''
        Creates and returns the complete transformation 
        matrix column-major format!

        I.e.:

        ( ROTATION               x_translation)
        (         MATRIX         y_translation)
        (                 HERE   z_translation)
        (0        0           0         1     )
        '''
        # ensure column-major format -> numpy thinks matrices have their
        # origin in the top left corner ...
        return ((Matrix44.from_scale(self.__scale) * self.__rotation_quaternion).T * Matrix44.from_translation(self.__translation))

    transformation_matrix = property(__get_transformation_matrix,)

    def __str__(self, *args, **kwargs):
        x = self.transformation_matrix
        pretty_matrix = "\n".join(map(str, [map(pretty_float, col) for col in [a_col.tolist() for a_col in [x.r1, x.r2, x.r3, x.r4]]])).replace("'", "").replace("[", "").replace("]", "")
        return "scale: {}\ntranslation: {}\nroatation:\n{}".format(map(pretty_float, self.scale), map(pretty_float, self.translation), pretty_matrix)
