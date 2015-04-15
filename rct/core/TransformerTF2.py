'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct.core.TransformListener import TransformListener
from rct.util import get_logger_by_class


# TODO: ABC this class
# base class in cpp: TransformerCore

class TransformerTF2(TransformListener):
    '''
    classdocs
    '''

    # TODO: IMPLEMENT

    __cache_time = None
    __logger = None

    def __init__(self, cache_time):
        '''
        Constructor
        '''
        self.__cache_time = cache_time
        self.__logger = get_logger_by_class(self.__class__)

    def new_transform_available(self, transform, is_static):
        self.__logger.info("LOL i got data: {}, {}".format(transform, is_static))


    def clear(self,):
        '''
        Clear all data
        '''
        pass

    def set_transform(self, transform, is_static=False):
        '''
         Add transform information to the rct data structure
        :param transform The transform to store
        :param authority The source of the information for this transform
        :param is_static Record this transform as a static transform.  It will be good across all time.  (This cannot be changed after the first call.)
        :return True unless an error occured
        '''

    def lookup_transform(self, target_frame, source_frame, time):
        '''
        Get the transform between two frames by frame ID.
        :param target_frame The frame to which data should be transformed
        :param source_frame The frame where the data originated
        :param time The time at which the value of the transform is desired. (0 will get the latest)
        :return The transform between the frames
        '''
        pass

    def lookup_transform2(self, target_frame, target_time, source_frame, source_time, fixed_frame):
        '''
        Get the transform between two frames by frame ID assuming fixed frame.
        :param target_frame The frame to which data should be transformed
        :param target_time The time to which the data should be transformed. (0 will get the latest)
        :param source_frame The frame where the data originated
        :param source_time The time at which the source_frame should be evaluated. (0 will get the latest)
        :param fixed_frame The frame in which to assume the transform is constant in time.
        :return The transform between the frames

        Possible exceptions tf2::LookupException, tf2::ConnectivityException,
        tf2::ExtrapolationException, tf2::InvalidArgumentException
        '''
        pass

    def request_transform(self, target_frame, source_frame, time):
        '''
        Request the transform between two frames by frame ID.
        :param target_frame The frame to which data should be transformed
        :param source_frame The frame where the data originated
        :param time The time at which the value of the transform is desired. (0 will get the latest)
        :return A future object representing the request status and transform between the frames
        '''
        # 'future object yada yada'
        pass


    def can_transform(self, target_frame, source_frame, time, error_msg):
        '''
        Test if a transform is possible
       :param target_frame The frame into which to transform
       :param source_frame The frame from which to transform
       :param time The time at which to transform
       :param error_msg A pointer to a string which will be filled with why the transform failed, if not NULL
       :return True if the transform is possible, false otherwise
        '''

    def can_transform2(self, target_frame, target_time, source_frame, source_time, fixed_frame, error_msg):
        '''
        Test if a transform is possible
        :param target_frame The frame into which to transform
        :param target_time The time into which to transform
        :param source_frame The frame from which to transform
        :param source_time The time from which to transform
        :param fixed_frame The frame in which to treat the transform as constant in time
        :param error_msg A pointer to a string which will be filled with why the transform failed, if not NULL
        :return True if the transform is possible, false otherwise
        '''

    def get_frame_strings(self):
        '''
        'A way to get a std::vector of available frame ids
        '''

    def frame_exists(self, frame_id_str):
        '''
        Check if a frame exists in the tree
        :param frame_id_str The frame id in question
        '''

    def get_parent(self, frame_id, time):
        '''
        Fill the parent of a frame.
        :param frame_id The frame id of the frame in question
        :param parent The reference to the string to fill the parent
        :return true unless "NO_PARENT" */
        '''

    def all_frames_as_dot(self):
        '''
        Backwards compatabilityA way to see what frames have been cached
        Useful for debugging
        '''

    def all_frames_as_YAML(self):
        '''
        A way to see what frames have been cached in yaml format
        Useful for debugging tools
        '''

    def all_frames_as_string(self):
        '''
        A way to see what frames have been cached
        Useful for debugging
        '''

    def convert_transform_to_tf(self, transform, transform_stamped):
        pass

    def convert_tf_to_transform(self, transform_stamped, transform):
        pass

    def print_contents(self):
        pass
