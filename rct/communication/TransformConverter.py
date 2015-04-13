'''
Created on Apr 13, 2015

@author: nkoester
'''
import time

from rsb.converter import Converter

class TransformConverter(Converter):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        # TODO FIX THIS!
        super(TransformConverter, self).__init__(bytearray, tuple, '.*')

    def serialize(self, data):
        # TODO !!
        return data[1], data[0]

    def deserialize(self, data, wireSchema):
        # TODO !!
        return wireSchema, data

    def domainToRST(self, transform , frame_transform):
        timestamp = time.time()

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

    def rstToDomain(self, frame_transform, transform):

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

