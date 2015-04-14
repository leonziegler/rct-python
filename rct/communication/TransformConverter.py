'''
Created on Apr 13, 2015

@author: nkoester
'''
import time

from rsb.converter import Converter, ProtocolBufferConverter
from rst.timing.Timestamp_pb2 import Timestamp

from rct.core.Transform import Transform
from rct.proto.FrameTransform_pb2 import FrameTransform


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

        frame_transform = self.domainToRST(data)
        serialized = self.__internal_converter.serialize(frame_transform)
        print "serialized: ", serialized

        return serialized


    def deserialize(self, data, wireSchema):

        wire_schema, frame_transform = self.__internal_converter.deserialize(data, wireSchema)
        transform = self.rstToDomain(frame_transform)
        return Transform, transform



    def domainToRST(self, transform):
        frame_transform = FrameTransform()

        frame_transform.frame_parent = transform.get_frame_parent()
        frame_transform.frame_child = transform.get_frame_child()
        frame_transform.time.time = int(time.time())

        # frame_transform.transform = None
        # TODO: IMPLEMENT
#         frame_transform.set_x(transform.getTranslation().x())
#         frame_transform.set_y(transform.getTranslation().y())
#         frame_transform.set_z(transform.getTranslation().z())
#         frame_transform.set_qw(transform.getRotationQuat().w())
#         frame_transform.set_qx(transform.getRotationQuat().x())
#         frame_transform.set_qy(transform.getRotationQuat().y())
#         frame_transform.set_qz(transform.getRotationQuat().z())

        return frame_transform

    def rstToDomain(self, frame_transform):
        # TODO: is this timestamp the right one? feels weird!
        transform = Transform(None, frame_transform.frame_parent(), frame_transform.frame_child(), time.time())

        # TODO: implement

        # TODO: numpy magic
        # f is frame_transform
        # Eigen::Vector3d p(t.transform().translation().x(), t.transform().translation().y(),
        # t.transform().translation().z());
        # Eigen::Quaterniond r(t.transform().rotation().qw(), t.transform().rotation().qx(), t.transform().rotation().qy(), t.transform().rotation().qz());
        # Eigen::Affine3d a = Eigen::Affine3d().fromPositionOrientationScale(p, r, Eigen::Vector3d::Ones());

#         a = None
#         transform.setTransform(a)

        return transform

