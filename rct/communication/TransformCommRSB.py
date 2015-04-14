'''
Created on Apr 13, 2015

@author: nkoester
'''
from rsb import Event, Scope
import rsb.converter

from rct.communication.TransformConverter import TransformConverter


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
    __scope_sync = "/rct/sync";
    __scope_transforms = "/rct/transform";
    __scope_suffix_static = "/static";
    __scope_suffix_dynamic = "/dynamic";
    __user_key_authority = "authority";

    __rsb_listener_transform = None
    __rsb_listener_sync = None
    __rsb_informer_transform = None
    __rsb_informer_sync = None

    __listeners = None

    # dict: { str : (rct.transform, rsb.metadata), }
    # str:
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


        self.__send_cache_dynamic = {}
        self.__send_cache_static = {}

    def init(self, transformer_config):
        '''
        Constructor.
        :param transformer_config:
        '''

        try:
            converter = TransformConverter()
            rsb.converter.registerGlobalConverter(converter)

        except RuntimeError:
            pass
        except Exception as e:
            print "ERROR: ", type(e), e

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
        '''
        Requests a sync of transformations from all others in the network.
        '''
        if self.__rsb_informer_sync:
            print "Sending sync request trigger from id {}".format(self.__rsb_informer_sync.getId())
            self.__rsb_informer_sync.publishData(None)
        else:
            raise Exception("communicator was not initialized!")


    def print_contents(self):
        print "authority: {}, communication: {}, #listeners: {}, #cache: {}".format(self.__authority, "RSB", len(self.__listeners), len(self.__send_cache_dynamic))

    def transform_handler(self, event):
        # aka transformCallback in cpp
        if event.getSenderId() == self.__rsb_informer_transform.getId():
            print "Received transform from myself. Ignore. (id :{})".format(str(event.getSenderId()))
            return

        authority = event.getMetaData().getUserInfo(self.__userKeyAuthority)
        # TODO implement

#    C++ code:
#     Scope staticScope = rsbInformerTransform->getScope()->concat(Scope(scopeSuffixStatic));
#     bool isStatic = (event->getScope() == staticScope);
#
#     t->setAuthority(authority);
#     RSCDEBUG(logger, "Received transform from " << authority);
#     RSCTRACE(logger, "Received transform: " << *t);
#
#     boost::mutex::scoped_lock(mutex);
#     vector<TransformListener::Ptr>::iterator it0;
#     for (it0 = listeners.begin(); it0 != listeners.end(); ++it0) {
#         TransformListener::Ptr l = *it0;
#         l->newTransformAvailable(*t, isStatic);
#     }


    def sync_handler(self, event):
        '''
        Handles data from the syncronisation source.

        The C++ counterpart is "triggerCallback"

        :param event: Incomming event
        '''

        if event.getSenderId() == self.__rsb_informer_sync.getId():
            print "Received transform from myself. Ignore. (id :{})".format(str(event.getSenderId()))
            return

        # TODO: thread this?
        self.publish_cache()

    def send_transform(self, transform, transform_type):
        '''
        Add transform information to the rct data structure.
        :param transform:
        :param transform_type:
        :return: True unless an error occured
        '''
        if not self.__rsb_informer_transform:
            print "RSB communicator was not initialized!"


        # TODO implement

        return True

    def publish_cache(self):

        for _, v in self.__send_cache_dynamic.iteritems():
            event = Event()
            event.setData(v[0])
            event.setScope(self.__rsb_informer_transform.getScope().contact(self.__scope_suffix_dynamic))
            event.setMetaData(v[1])
            self.__rsb_informer_transform.publishEvent(event)

        for _, v in self.__send_cache_static.iteritems():
            event = Event()
            event.setData(v[0])
            event.setScope(self.__rsb_informer_transform.getScope().contact(self.__scope_suffix_static))
            event.setMetaData(v[1])
            self.__rsb_informer_transform.publishEvent(event)
