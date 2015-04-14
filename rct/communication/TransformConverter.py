'''
Created on Apr 13, 2015

@author: nkoester
'''
import time

from rsb.converter import Converter, ProtocolBufferConverter

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
        super(TransformConverter, self).__init__(bytearray, type(FrameTransform), type(Transform))
        __internal_converter = ProtocolBufferConverter(FrameTransform)


    def serialize(self, data):
        domain = data[1]
        frame_transform = self.domainToRST(domain)

        return type(frame_transform), self.__internal_converter.serialize(frame_transform)



    def deserialize(self, data, wireSchema):

        convertee = self.__internal_converter.deserialize(data, wireSchema)
        frame_transform = convertee[1]
        transform = self.rstToDomain(frame_transform)

#         return wireSchema, transform
        return convertee[0], transform



    def domainToRST(self, transform):
        frame_transform = FrameTransform()
        timestamp = time.time()
        return frame_transform

        # TODO: IMPLEMENT

        frame_transform.set_frame_parent(transform.getFrameParent());
        frame_transform.set_frame_child(transform.getFrameChild())

        frame_transform.set_time(timestamp)

        frame_transform.set_x(transform.getTranslation().x())
        frame_transform.set_y(transform.getTranslation().y())
        frame_transform.set_z(transform.getTranslation().z())
        frame_transform.set_qw(transform.getRotationQuat().w())
        frame_transform.set_qx(transform.getRotationQuat().x())
        frame_transform.set_qy(transform.getRotationQuat().y())
        frame_transform.set_qz(transform.getRotationQuat().z())

        return frame_transform

    def rstToDomain(self, frame_transform):
        transform = Transform()

        return transform

        # TODO: FIXX
        timestamp = time.time()

        # TODO: numpy magic
        # f is frame_transform
        # Eigen::Vector3d p(t.transform().translation().x(), t.transform().translation().y(),
        # t.transform().translation().z());
        # Eigen::Quaterniond r(t.transform().rotation().qw(), t.transform().rotation().qx(), t.transform().rotation().qy(), t.transform().rotation().qz());
        # Eigen::Affine3d a = Eigen::Affine3d().fromPositionOrientationScale(p, r, Eigen::Vector3d::Ones());
        a = None


        transform.setFrameParent(frame_transform.frame_parent())
        transform.setFrameChild(frame_transform.frame_child())
        transform.setTime(timestamp)
        transform.setTransform(a)

        return transform

