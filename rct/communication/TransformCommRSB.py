'''
Created on Apr 13, 2015

@author: nkoester
'''
import logging

from rsb import Event, Scope, MetaData
import rsb.converter

from rct.communication.TransformConverter import TransformConverter
from rct.core.Transform import Transform
from rct.util import TransformType, get_logger_by_class


# TODO: use abc for this class...
#
# import abc
#
# class TransformCommunicator(object):
#     __metaclass__ = abc.ABCMeta
#
#     @abc.abstractproperty
#     ...
# aintnobodygottimeforthat

class TransformCommRSB(object):

    '''
    classdocs
    '''

    __authority = None
    __scope_sync = "/rct/sync"
    __scope_transforms = "/rct/transform"
    __scope_suffix_static = "/static"
    __scope_suffix_dynamic = "/dynamic"
    __user_key_authority = "authority"

    __rsb_listener_transform = None
    __rsb_listener_sync = None
    __rsb_informer_transform = None
    __rsb_informer_sync = None

    __listeners = None

    __transform_converter = None

    # dict: { str : (rct.transform, rsb.metadata), }
    __send_cache_dynamic = None
    # dict: { str : (rct.transform, rsb.metadata), }
    __send_cache_static = None

    __transformer_config = None

    __logger = None

    def __init__(self,
                 authority,
                 transform_listeners=None,
                 scope_sync=None,
                 scope_transforms=None,
                 scope_suffix_static=None,
                 scope_suffix_dynamic=None,
                 user_key_authority=None):
        '''
        Constructor
        '''

        self.__listeners = []
        if transform_listeners:
            self.add_transform_listeners(transform_listeners)

        self.__authority = authority

        if scope_sync:
            self.__scope_sync = scope_sync
        if scope_transforms:
            self.__scope_transforms = scope_transforms
        if scope_suffix_static:
            self.__scope_suffix_static = scope_suffix_static
        if scope_suffix_dynamic:
            self.__scope_suffix_dynamic = scope_suffix_dynamic
        if user_key_authority:
            self.__user_key_authority = user_key_authority

        self.__send_cache_dynamic = {}
        self.__send_cache_static = {}

        self.__logger = get_logger_by_class(self.__class__)

    def init(self, transformer_config):
        '''
        Constructor.
        :param transformer_config:
        '''

        try:
            if not self.__transform_converter:
                self.__transform_converter = TransformConverter()
            rsb.converter.registerGlobalConverter(self.__transform_converter)
        except RuntimeError as _:
            self.__logger.debug("[{}] Converter already registered. Ignoring.".format(self.__authority))
        except Exception as e:
            self.__logger.exception(e)

        # TODO: what about the config?!
        # self.__transformer_config = transformer_config

        self.__rsb_listener_transform = rsb.createListener(self.__scope_transforms)
        self.__rsb_listener_sync = rsb.createListener(self.__scope_sync)
        self.__rsb_informer_transform = rsb.createInformer(self.__scope_transforms)
        self.__rsb_informer_sync = rsb.createInformer(self.__scope_sync)

        self.__rsb_listener_transform.addHandler(self.transform_handler)
        self.__rsb_listener_sync.addHandler(self.sync_handler)

        self.__logger.debug("[{}] RSB setup:\nListeners:\n\t{} @ {}\n\t{} @ {}\nInformers:\n\t{} @ {}\n\t{} @ {}\n".format(self.__authority,
                                                                                                                           self.__rsb_listener_transform.getId(), self.__rsb_listener_transform.scope,
                                                                                                                           self.__rsb_listener_sync.getId(), self.__rsb_listener_sync.scope,
                                                                                                                           self.__rsb_informer_transform.getId(), self.__rsb_informer_transform.scope,
                                                                                                                           self.__rsb_informer_sync.getId(), self.__rsb_informer_sync.scope))

        self.request_sync()

    def shutdown(self):
        '''
        Cleans up all RSB connections.
        '''
        for a_listener in self.listeners:
            try:
                a_listener.listener.deactivate()
            except Exception, e:
                self.__logger.error("[{}] Error during rsb listener shutdown: %s".format(self.__authority, str(e)))

        self.__rsb_listener_transform.deactivate()
        self.__rsb_listener_sync.deactivate()
        self.__rsb_informer_transform.deactivate()
        self.__rsb_informer_sync.deactivate()

    def add_transform_listener(self, transform_listener):
        # TODO: use a lock here?
        self.__listeners.append(transform_listener)

    def add_transform_listeners(self, transform_listeners):
        '''

        :param transform_listeners: list of transform listeners
        '''
        # TODO: use a lock here?
        for a_transform_listener in transform_listeners:
            self.__listeners.append(a_transform_listener)

    def remove_transform_listener(self, transform_listener):
        try:
            self.__listeners.remove(transform_listener)
        except ValueError:
            pass

    def send_transforms(self, transforms, transform_type):
        '''

        :param transforms: list of transformation
        :param type:
        '''
        for a_transform in transforms:
            self.send_transform(a_transform, transform_type)
        return True

    def get_authority_name(self):
        return self.__authority

    def get_config(self):
        return self.__transformer_config

    def request_sync(self):
        '''
        Requests a sync of transformations from all others in the network.
        '''
        if self.__rsb_informer_sync:
            self.__logger.info("[{}] Sending sync request trigger from id {}".format(self.__authority, self.__rsb_informer_sync.getId()))
            self.__rsb_informer_sync.publishData(None)
        else:
            raise Exception("communicator was not initialized!")

    def print_contents(self, level=logging.INFO):
        self.__logger.log(level, "authority: {}, communication: {}, #listeners: {}, #cache: {}".format(self.__authority, "RSB", len(self.__listeners), len(self.__send_cache_dynamic)))

    def transform_handler(self, event):
        '''
        Handles incoming transformation updates.

        The C++ counterpart is "transformCallback"

        :param event:Incoming event
        '''
        if event.getSenderId() == self.__rsb_informer_transform.getId():
            self.__logger.debug("[{}] Received transform update from myself. Ignore. (id: {})".format(self.__authority, str(event.getSenderId())))
            return

        # data is of type rct.core.Transform
        data = event.getData()
        if not isinstance(data, Transform):
            self.__logger.warning("[{}] Incoming data is of type {} (expected {}). Ignore.".format(self.__authority, type(data), Transform))
            return

        try:
            received_authority = event.getMetaData().userInfos[self.__user_key_authority]
            static_scope = self.__rsb_informer_transform.getScope().concat(Scope(self.__scope_suffix_static))

            is_static = event.scope == static_scope

            data.set_authority(received_authority)
            self.__logger.info("[{}] Received transform from '{}': {}".format(self.__authority, received_authority, data))

            # TODO: threaded?
            for a_listener in self.__listeners:
                a_listener.new_transform_available(data, is_static)

        except KeyError as ke:
            self.__logger.warning("[{}] ERROR during data handling: Cannot find neccessary key '{}' in meta data user info field of event! Actual content: {}".format(self.__authority, ke, event.metaData))
        except Exception as e:
            self.__logger.exception("[{}] ERROR during data handling: {}".format(self.__authority, str(e)))

    def send_transform(self, transform, transform_type):
        '''
        Add transform information to the rct data structure.
        :param transform:
        :param transform_type:
        :return: True unless an error occured
        '''

        if not self.__rsb_informer_transform:
            self.__logger.error("[{}] RSB communicator was not initialized!".format(self.__authority))

        # some small type checks for usability
        assert isinstance(transform, Transform), "Input transformation has to be of type rct.Transform! (Input was: {})".format(type(transform))
        assert hasattr(TransformType, transform_type), "Input transformation type has to be of type rct.TransformType! (Input was: {})".format(type(transform_type))

        cache_key = transform.get_frame_parent() + transform.get_frame_child()
        meta_data = MetaData()

        if transform.get_authority() is "":
            meta_data.setUserInfo(self.__user_key_authority, self.__authority)
        else:
            meta_data.setUserInfo(self.__user_key_authority, transform.get_authority())

        self.__logger.info("[{}] Publishing transform from {}".format(self.__authority, self.__rsb_informer_transform.getId()))

        # TODO: threaded?
        event = Event()
        event.setData(transform)
        event.setType(type(transform))
        event.setMetaData(meta_data)

        if transform_type is TransformType.STATIC:
            self.__send_cache_static[cache_key] = (transform, meta_data)
            event.setScope(self.__rsb_informer_transform.getScope().concat(Scope(self.__scope_suffix_static)))

        elif transform_type is TransformType.DYNAMIC:
            self.__send_cache_dynamic[cache_key] = (transform, meta_data)
            event.setScope(self.__rsb_informer_transform.getScope().concat(Scope(self.__scope_suffix_dynamic)))

        else:
            self.__logger.error("[{}] Cannot send transform. Reason: Unknown TransformType: {}".format(self.__authority, str(transform_type)))
            return False

        self.__logger.info("[{}] Sending {} to scope {}".format(self.__authority, transform.__str__(), event.getScope()))
        self.__rsb_informer_transform.publishEvent(event)
        self.__logger.debug("[{}] Sending successful!".format(self.__authority))

        return True

    def sync_handler(self, event):
        '''
        Handles data from the syncronisation source.

        The C++ counterpart is "triggerCallback"

        :param event: Incoming event
        '''

        if event.getSenderId() == self.__rsb_informer_sync.getId():
            self.__logger.debug("[{}] Received sync request from myself. Ignore. (id: {})".format(self.__authority, str(event.getSenderId())))
            return

        # TODO: thread this?
        self.publish_cache()

    def publish_cache(self):
        self.__logger.info("[{}] Publishing cache... ({} total)".format(self.__authority, len(self.__send_cache_dynamic.keys()) + len(self.__send_cache_static.keys())))
        for _, v in self.__send_cache_dynamic.iteritems():
            event = Event()
            event.setData(v[0])
            event.setType(type(v[0]))
            event.setScope(self.__rsb_informer_transform.getScope().concat(Scope(self.__scope_suffix_dynamic)))
            event.setMetaData(v[1])
            self.__rsb_informer_transform.publishEvent(event)

        for _, v in self.__send_cache_static.iteritems():
            event = Event()
            event.setData(v[0])
            event.setType(type(v[0]))
            event.setScope(self.__rsb_informer_transform.getScope().concat(Scope(self.__scope_suffix_static)))
            event.setMetaData(v[1])
            self.__rsb_informer_transform.publishEvent(event)
