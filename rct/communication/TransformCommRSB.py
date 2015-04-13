'''
Created on Apr 13, 2015

@author: nkoester
'''
from rct.communication.TransformConverter import TransformConverter
import rsb

# TODO: use abc for this class...
#
# import abc
#
# class TransformCommunicator(object):
#     __metaclass__ = abc.ABCMeta
#
#     @abc.abstractproperty
#     ...

class TransformCommRSB(object):
    '''
    classdocs
    '''

    __authority = None
    __scope_sync = "/rct/sync";
    __scope_transforms = "/rct/transform";
    __scope_suffic_static = "/static";
    __scope_suffix_dynamic = "/dynamic";
    __user_key_authority = "authority";

    __rsb_listener_transform = None
    __rsb_listener_sync = None
    __rsb_informer_transform = None
    __rsb_informer_sync = None

    __listeners = None

    # dict: { str : (rct.transform, rsb.metadata), }
    __send_cache_dynamic = None
    __send_cache_static = None

    __transformer_config = None

    def __init__(self,
                 authority,
                 transform_listener=None,
                 scope_sync=None,
                 scope_transforms=None,
                 scope_suffic_static=None,
                 scope_suffix_dynamic=None,
                 user_key_authority=None):
        '''
        Constructor
        '''

        self.__listeners = []
        if transform_listener:
            self.add_transform_listener(transform_listener)

        self.__authority = authority

        if scope_sync:
            self.__scope_sync = scope_sync
        if scope_transforms:
            self.__scope_transforms = scope_transforms
        if scope_suffic_static:
            self.__scope_suffic_static = scope_suffic_static
        if scope_suffix_dynamic:
            self.__scope_suffix_dynamic = scope_suffix_dynamic
        if user_key_authority:
            self.__user_key_authority = user_key_authority


        __send_cache_dynamic = {}
        __send_cache_static = {}

    def init(self, transformer_config):
        '''
        Constructor.
        :param transformer_config:
        '''

        try:
            # TODO: is this correcT?
            converter = TransformConverter()
            # converter = rsb.converter.ProtocolBufferConverter(messageClass=TransformConverter)
            rsb.converter.registerGlobalConverter(converter)

        except Exception, e:
            print "ERROR: Converter already present", e

        # TODO: what about the config?!
        # self.__transformer_config = transformer_config

        self.__rsb_listener_transform = rsb.createListener(self.__scope_transforms)
        self.__rsb_listener_sync = rsb.createListener(self.__scope_sync)
        self.__rsb_informer_transform = rsb.createInformer(self.__scope_transforms)
        self.__rsb_informer_sync = rsb.createInformer(self.__scope_sync)


        self.__rsb_listener_transform.addHandler(self.transform_handler)
        self.__rsb_listener_sync.addHandler(self.sync_handler)

        self.request_sync()

    def shutdown(self):
        '''
        Cleans up all RSB connections.
        '''
        for a_listener in self.listeners:
            try:
                a_listener.listener.deactivate()
            except Exception, e:
                self.log.error("Error during rsb listener shutdown: %s", str(e))

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
        pass

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

        if not self.__rsb_informer_sync:
            raise Exception("communicator was not initialized!")
        else:

            print "Sending sync request trigger from id {}".format(self.__rsb_informer_sync.getId().getAsUUID())
            # trigger other instances to send transforms
            # TODO: what to publish here?
            self.__rsb_informer_sync.publish()
            # rsbInformerSync->publish(shared_ptr<void>());

    def print_contents(self):
        print "authority: {}, communication: {}, #listeners: {}, #cache: {}".format(self.__authority, "RSB", len(self.__listeners), len(self.__send_cache_dynamic))

    def transform_handler(self):
        # TODO implement
        pass

    def sync_handler(self):
        # TODO implement
        pass

    def send_transform(self, transform, transform_type):
        '''
        Add transform information to the rct data structure.
        :param transform:
        :param transform_type:
        '''
        # TODO implement
        return True

    def transform_callback(self, event):
        # TODO implement
        pass

    def trigger_callback(self, event):
        # TODO implement
        pass

    def publish_cache(self):
        # TODO implement
        pass
