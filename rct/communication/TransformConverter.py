'''
Created on Apr 13, 2015

@author: nkoester
'''
import time

from rsb.converter import Converter, ProtocolBufferConverter

from rct.core.Transform import Transform
from rct.proto.FrameTransform_pb2 import FrameTransform
from rct.core.Affine3d import Affine3d


class TransformConverter(Converter):

    '''
    classdocs
    '''

    __internal_converter = None

    def __init__(self):
        '''
        Constructor
        '''
        # TODO FIX THIS!
        self.__internal_converter = ProtocolBufferConverter(FrameTransform)
        super(TransformConverter, self).__init__(bytearray, Transform, self.__internal_converter.getWireSchema())

    def serialize(self, data):
        frame_transform = self.domain_to_RST(data)
        serialized = self.__internal_converter.serialize(frame_transform)
        return serialized

    def deserialize(self, data, wireSchema):
        frame_transform = self.__internal_converter.deserialize(data, wireSchema)
        transform = self.rst_to_domain(frame_transform)
        return transform

    def domain_to_RST(self, transform):
        frame_transform = FrameTransform()
        frame_transform.frame_parent = transform.get_frame_parent()
        frame_transform.frame_child = transform.get_frame_child()
        frame_transform.time.time = int(time.time())
        frame_transform.transform.translation.x = transform.get_translation()[0]
        frame_transform.transform.translation.y = transform.get_translation()[1]
        frame_transform.transform.translation.z = transform.get_translation()[2]
        frame_transform.transform.rotation.qw = transform.get_rotation_quat()[0]
        frame_transform.transform.rotation.qx = transform.get_rotation_quat()[1]
        frame_transform.transform.rotation.qy = transform.get_rotation_quat()[2]
        frame_transform.transform.rotation.qz = transform.get_rotation_quat()[3]
        return frame_transform

    def rst_to_domain(self, frame_transform):

        position_vector = (frame_transform.transform.translation.x,
                           frame_transform.transform.translation.y,
                           frame_transform.transform.translation.z)

        rotation_quaterniond = (frame_transform.transform.rotation.qw,
                                frame_transform.transform.rotation.qx,
                                frame_transform.transform.rotation.qy,
                                frame_transform.transform.rotation.qz)

        new_transformation = Affine3d(position_vector, rotation_quaterniond, (1, 1, 1))

        # TODO: is this timestamp the right one? feels weird!
        transform = Transform(new_transformation,
                              frame_transform.frame_parent,
                              frame_transform.frame_child,
                              time.time())

        # new_transformation = None
        # TODO: implement with numpy magic
        # f is frame_transform

#         Eigen::Vector3d p(t.transform().translation().x(),
#                           t.transform().translation().y(),
#                           t.transform().translation().z());

#         Eigen::Quaterniond r(t.transform().rotation().qw(),
#                              t.transform().rotation().qx(),
#                              t.transform().rotation().qy(),
#                              t.transform().rotation().qz());

        # Eigen::Affine3d a = Eigen::Affine3d().fromPositionOrientationScale(p, r, Eigen::Vector3d::Ones());

        return transform
