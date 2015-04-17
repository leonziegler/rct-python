'''
Created on Apr 13, 2015

@author: nkoester
'''
import logging


class CommunicatorType(object):

    '''
    Enum fake.
    '''
    AUTO = "AUTO"
    RSB = "RSB"
    ROS = "ROS"


class TransformType(object):

    '''
    Enum fake.
    '''
    STATIC = "STATIC"
    DYNAMIC = "DYNAMIC"


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def get_logger_by_class(klass):
    """
    Taken from RSB python implementation.

    See http://docs.cor-lab.de//rsb-manual/trunk/html/index.html

    Get a python logger instance based on a class instance. The logger name will
    be a dotted string containing python module and class name.

    @author: jwienke
    @param klass: class instance
    @return: logger instance
    """
    return logging.getLogger(klass.__module__ + "." + klass.__name__)


def pretty_float(a_float):
    '''
    Returns pretty pretty floats
    '''
    return "%0.3f" % a_float
