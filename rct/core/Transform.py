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

    __transform = None
    __frame_parent = None
    __frame_child = None
    __timestamp = None
    __authority = None
    __logger = None

    def __init__(self, transform, frame_parent, frame_child, timestamp, authority=""):
        '''
        Constructor
        '''
        assert isinstance(
            transform, Affine3d), "Transform has to be of type rct.core.Affine3d!"

        self.__transform = transform
        self.__frame_parent = frame_parent
        self.__frame_child = frame_child
        self.__timestamp = timestamp
        self.__authority = authority
        self.__logger = get_logger_by_class(self.__class__)

    def get_rotation_YPR(self):
        # TODO: Implement
        raise NotImplementedError()
#     const Eigen::Vector3d getRotationYPR() const {
#
#         Eigen::Matrix3d mat = transform.rotation().matrix();
#
#         // this code is taken from buttel btMatrix3x3 getEulerYPR().
#         // http://bulletphysics.org/Bullet/BulletFull/btMatrix3x3_8h_source.html
#         // first use the normal calculus
#         double yawOut = atan2(mat(1,0), mat(0,0));
#         double pitchOut = asin(-mat(2,0));
#         double rollOut = atan2(mat(2,1), mat(2,2));
#
#         // on pitch = +/-HalfPI
#         if (abs(pitchOut) == M_PI / 2.0) {
#             if (yawOut > 0)
#                 yawOut -= M_PI;
#             else
#                 yawOut += M_PI;
#             if (pitchOut > 0)
#                 pitchOut -= M_PI;
#             else
#                 pitchOut += M_PI;
#         }
#         return Eigen::Vector3d(yawOut, pitchOut, rollOut);
#     }

    def get_rotation_matrix(self):
        return self.__transform.get_rotation_matrix()

    def get_transformation_matrix(self):
        return self.__transform.get_transformation_matrix()

    def get_translation_matrix(self):
        return self.__transform.get_translation_matrix()

    def get_translation(self):
        return self.__transform.translation

    translation = property(get_translation, )

    def get_rotation_quaternion(self):
        return self.__transform.rotation_quaternion

    rotation_quaternion = property(get_rotation_quaternion, )

    def set_frame_parent(self, frame_parent):
        self.__frame_parent = frame_parent

    def get_frame_parent(self):
        return self.__frame_parent

    def set_frame_child(self, frame_child):
        self.__frame_child = frame_child

    def get_frame_child(self):
        return self.__frame_child

    def set_authority(self, authority):
        self.__authority = authority

    def get_authority(self):
        return self.__authority

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def get_timestamp(self):
        return self.__timestamp

    def print_contents(self, level=logging.INFO):
        self.__logger.log(level, "authority: {}, frame_parent: {}, frame_child: {}, timestamp: {}, transform: {}".format(
            self.__authority, self.__frame_parent, self.__frame_child, self.__timestamp, self.__transform))

    def __str__(self, *args, **kwargs):
        return "parent: {}, child: {}, time: {}, transform: {}".format(self.__frame_parent, self.__frame_child, int(self.__timestamp), self.__transform)

    def get_transform(self):
        return self.__transform

    def set_transform(self, value):
        self.__transform = value
    transform = property(get_transform, set_transform)
