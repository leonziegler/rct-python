#!/usr/bin/python

'''
Created on Apr 17, 2015

@author: nkoester
'''

# Imports
import logging
import time
from pyrr import Quaternion, Matrix44, Vector3, Vector4, Matrix33

import numpy as np
np.set_printoptions(precision=4)

import rct

# allows to CTRL+c
import signal
from rct.core.Affine3d import Affine3d
from rct.core.Transform import Transform
doRun = True


def signal_handler(signal, frame):
    global doRun
    print "exiting."
    doRun = False
signal.signal(signal.SIGINT, signal_handler)


# our subscriber
tf2_subscriber = rct.TransformerFactory().create_transform_receiver()


def calculate_transformation_now(target, source, point):
    when = time.time()
    time.sleep(0.3)
    print ">> %s -> %s" % (source, target)
    if tf2_subscriber.can_transform(target, source, when):
        transform = tf2_subscriber.lookup_transform(target, source, when)
        transformed_point = transform.transformation.apply_transformation(point)

        return transformed_point
    else:
        print "ERROR: %s -> %s not available!" % (source, target)
        return None


if __name__ == '__main__':

    # Configure logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.getLogger('rsb').setLevel(logging.WARNING)
    logging.getLogger('rct').setLevel(logging.INFO)

    print "\n>> Gathering transformation info ..."
    time.sleep(1)

    print ">> Currently available transformations:\n"
    print "\n\t".join(("\t" + tf2_subscriber.all_frames_as_string()).split('\n'))

    # a point in space we want to transform
    source_point4 = Vector4([1., 1., 1., 1.])

    print "Base point: ", source_point4
    print "--------------------------------\n"

    # automatic search for trafos...
#     available_trafos = tf2_subscriber.all_frames_as_string().split('\n')
#     mappings_to_do = []
#     for x in available_trafos:
#         if len(x) > 3:
#             x = x.replace("Frame ", "")
#             x = x.replace(" exists with parent ", ",")
#             x = x[:-1]
#             res = x.split(",")
#             mappings_to_do.append([res[1], res[0]])

    mappings_to_do = [['base', 'python_static'],
                      ['base', 'python_dynamic'],
                      ['base', 'java_static'],
                      ['base', 'java_dynamic'],
                      ]
    for k in mappings_to_do:
        transformed_point = calculate_transformation_now(k[1], k[0], source_point4)
        print source_point4, "-->", transformed_point
        re_transformed_point = calculate_transformation_now(k[0], k[1], transformed_point)
        print transformed_point, "-->", re_transformed_point, "\n"
