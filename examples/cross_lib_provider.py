#!/usr/bin/python

'''
Created on Apr 17, 2015

@author: nkoester
'''

# Imports
import logging
import time

from pyrr import Quaternion, Matrix44, Vector4
import pyrr

import numpy as np
np.set_printoptions(precision=4)
import rct

# allows to CTRL+c
import signal
doRun = True


def signal_handler(signal, frame):
    global doRun
    print "exiting."
    doRun = False
signal.signal(signal.SIGINT, signal_handler)


def provide_static_transformation(tf2_publisher):

    # translate along the x axis
    translation = Vector4([1., 0., -1., 0.])

    # rotate around x by 90 degrees
    rotation = Quaternion.from_z_rotation((np.pi / 2))

    # with normal scaling
    scale = Vector4([1., 1., 1., 1.])

    # combine the above
    af_s = rct.Affine3d(translation, rotation, scale)

    # actually send it
    t_s = rct.Transform(af_s, "base", "python_static", time.time())
    print ">> providing STATIC: "
    print "YRP         : ", t_s.transformation.yrp
    print "translation : ", t_s.transformation.translation
    print "rotation    : ", t_s.transformation.rotation_quaternion
    tf2_publisher.send_transform(t_s, rct.TransformType.STATIC)


def provide_dynamic_transformation(tf2_publisher):

    # construct the dynamic transformation
    rotation = Quaternion.from_z_rotation(np.pi / 2)

    # with normal scaling
    scale = Vector4([1., 1., 1., 1.])

    # translate again along x
    position = Vector4([0., -1., 2., 0.])

    af_d = rct.Affine3d(position, rotation, scale)
    t_d = rct.Transform(af_d, "python_static", "python_dynamic", time.time())

    print ">> providing DYNAMIC: "
    print "YRP         : ", t_d.transformation.yrp
    print "translation : ", t_d.transformation.translation
    print "rotation    : ", t_d.transformation.rotation_quaternion

    logging.getLogger('rct').setLevel(logging.WARNING)
    # actually send it
    while(doRun):
        tf2_publisher.send_transform(t_d, rct.TransformType.DYNAMIC)
        time.sleep(0.019)


if __name__ == '__main__':

    # Configure logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.getLogger('rsb').setLevel(logging.WARNING)
    logging.getLogger('rct').setLevel(logging.WARNING)

    # our publisher
    tf2_publisher = rct.TransformerFactory().create_transform_publisher("python_provider")

    print "\n\n>> sending static transformation base->python ..."
    # provide our static transformation
    provide_static_transformation(tf2_publisher)

    print "\n>> sending constant dynamic transformation python->python_dynamic ..."
    # continiously provide our dynamic transformation
    provide_dynamic_transformation(tf2_publisher)
