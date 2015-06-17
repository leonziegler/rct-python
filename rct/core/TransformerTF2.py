'''
Created on Apr 13, 2015

@author: nkoester
'''
import geometry_msgs.msg
import logging
import rospy
import tf2_py
import time

from rct.core.Transform import Transform
from rct.core.TransformListener import TransformListener
from rct.util import get_logger_by_class
from rct.core.Affine3d import Affine3d
from pyrr import Quaternion, Vector4


class TransformerTF2(TransformListener):

    '''
    Simple wrapper class for tf_py.
    '''

    __logger = None
    __tf_core = None

    def __init__(self, cache_time):
        '''
        Constructor
        '''
        self.__logger = get_logger_by_class(self.__class__)
        self.__tf_core = tf2_py.BufferCore(rospy.Duration(cache_time))

    def new_transform_available(self, transform, is_static):
        '''
        See Meta Class.
        '''
        self.set_transform(transform, is_static)

    def set_transform(self, transform, is_static=False):
        '''
         Add transform information to the rct data structure
        :param transform The transform to store
        :param authority The source of the information for this transform
        :param is_static Record this transform as a static transform.
               It will be good across all time.  (This cannot be changed after
               the first call.)
        :return True unless an error occured
        '''
        tf_transform = self.convert_transform_to_tf(transform)

        if is_static:
            self.__tf_core.set_transform_static(
                tf_transform, transform.get_authority())
        else:
            self.__tf_core.set_transform(
                tf_transform, transform.get_authority())

    def lookup_transform(self, target_frame, source_frame, time):
        '''
        Get the transform between two frames by frame ID.
        :param target_frame The frame to which data should be transformed
        :param source_frame The frame where the data originated
        :param time The time at which the value of the transform is desired.
               (0 will get the latest)
        :return The transform between the frames
        '''
        tf_transform = self.__tf_core.lookup_transform_core(target_frame, source_frame, rospy.Time.from_sec(time))
        transform = self.convert_tf_to_transform(tf_transform)
        return transform

    def lookup_transform_full(self, target_frame, target_time, source_frame, source_time, fixed_frame):
        '''
        Get the transform between two frames by frame ID assuming fixed frame.
        :param target_frame The frame to which data should be transformed
        :param target_time The time to which the data should be transformed.
               (0 will get the latest)
        :param source_frame The frame where the data originated
        :param source_time The time at which the source_frame should be
               evaluated. (0 will get the latest)
        :param fixed_frame The frame in which to assume the transform is
               constant in time.
        :return The transform between the frames

        Possible exceptions:
        tf2::LookupException, tf2::ConnectivityException,
        tf2::ExtrapolationException, tf2::InvalidArgumentException
        '''

        tf_transform = self.__tf_core.lookup_transform_full_core(target_frame, rospy.Time.from_sec(
            target_time), source_frame, rospy.Time.from_sec(source_time), fixed_frame)
        transform = self.convert_tf_to_transform(tf_transform)
        return transform

    def can_transform(self, target_frame, source_frame, time):
        '''
        Test if a transform is possible
       :param target_frame The frame into which to transform
       :param source_frame The frame from which to transform
       :param time The time at which to transform
       :return True if the transform is possible, false otherwise
        '''
        return self.__tf_core.can_transform_core(target_frame, source_frame, rospy.Time.from_sec(time))

    def can_transform_full(self, target_frame, target_time, source_frame, source_time, fixed_frame):
        '''
        Test if a transform is possible
        :param target_frame The frame into which to transform
        :param target_time The time into which to transform
        :param source_frame The frame from which to transform
        :param source_time The time from which to transform
        :param fixed_frame The frame in which to treat the transform as 
               constant in time
        :return True if the transform is possible, false otherwise
        '''
        return self.__tf_core.can_transform_full_core(target_frame, rospy.Time.from_sec(target_time), source_frame, rospy.Time.from_sec(source_time), fixed_frame)

    def all_frames_as_YAML(self):
        '''
        A way to see what frames have been cached in yaml format
        Useful for debugging tools
        '''
        return self.__tf_core.all_frames_as_yaml()

    def all_frames_as_string(self):
        '''
        A way to see what frames have been cached
        Useful for debugging
        '''
        return self.__tf_core.all_frames_as_string()

    def convert_transform_to_tf(self, transform):
        transform_stamped = geometry_msgs.msg.TransformStamped()
        transform_stamped.header.frame_id = transform.frame_parent
        transform_stamped.header.stamp = rospy.Time.from_sec(time.time())
        transform_stamped.child_frame_id = transform.frame_child
        transform_stamped.transform.rotation.w = transform.transformation.rotation_quaternion.w
        transform_stamped.transform.rotation.x = transform.transformation.rotation_quaternion.x
        transform_stamped.transform.rotation.y = transform.transformation.rotation_quaternion.y
        transform_stamped.transform.rotation.z = transform.transformation.rotation_quaternion.z
        transform_stamped.transform.translation.x = transform.transformation.translation.x
        transform_stamped.transform.translation.y = transform.transformation.translation.y
        transform_stamped.transform.translation.z = transform.transformation.translation.z
        return transform_stamped

    def convert_tf_to_transform(self, transform_stamped):
        position_vector = Vector4()
        position_vector.x = transform_stamped.transform.translation.x
        position_vector.y = transform_stamped.transform.translation.y
        position_vector.z = transform_stamped.transform.translation.z
        position_vector.w = 0.

        rotation_quaterniond = Quaternion()
        rotation_quaterniond.w = transform_stamped.transform.rotation.w
        rotation_quaterniond.x = transform_stamped.transform.rotation.x
        rotation_quaterniond.y = transform_stamped.transform.rotation.y
        rotation_quaterniond.z = transform_stamped.transform.rotation.z

        scale = Vector4([1., 1., 1., 1.])

        affine3d = Affine3d(position_vector, rotation_quaterniond, scale)

        transform = Transform(affine3d,
                              transform_stamped.header.frame_id,
                              transform_stamped.child_frame_id,
                              transform_stamped.header.stamp.to_time(),
                              authority="")
        return transform

    def print_contents(self, level=logging.INFO):
        self.__logger.log(level, "backend = tf2_py.BufferCore")

    def clear(self,):
        '''
        Clears all data.
        '''
        self.__tf_core.clear()

    ####################################################################
    #   All of the following seem not to be wrapped by tf_py ... :(    #
    ####################################################################

    def get_frame_strings(self):
        '''
        'A way to get a std::vector of available frame ids
        '''
        raise NotImplementedError()

    def frame_exists(self, frame_id_str):
        '''
        Check if a frame exists in the tree
        :param frame_id_str The frame id in question
        '''
        raise NotImplementedError()

    def get_parent(self, frame_id, time):
        '''
        Fill the parent of a frame.
        :param frame_id The frame id of the frame in question
        :param parent The reference to the string to fill the parent
        :return true unless "NO_PARENT"
        '''
        raise NotImplementedError()

    def all_frames_as_dot(self):
        '''
        Backwards compatabilityA way to see what frames have been cached
        Useful for debugging
        '''
        raise NotImplementedError()

    def request_transform(self, target_frame, source_frame, time):
        '''
        Request the transform between two frames by frame ID.
        :param target_frame The frame to which data should be transformed
        :param source_frame The frame where the data originated
        :param time The time at which the value of the transform is desired.
               (0 will get the latest)
        :return A future object representing the request status and transform
                between the frames
        '''
        raise NotImplementedError()
