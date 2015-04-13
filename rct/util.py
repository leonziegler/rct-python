'''
Created on Apr 13, 2015

@author: nkoester
'''

class CommunicatorType(object):
    '''
    Enum fake.
    '''
    AUTO = "AUTO"
    RSB = "RSB"
    ROS = "ROS"

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
