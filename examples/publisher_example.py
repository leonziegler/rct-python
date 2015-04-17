#!/usr/bin/python

'''
Created on Apr 17, 2015

@author: nkoester
'''

# Imports
import logging
import time

from pyrr import Quaternion, Matrix44, Vector3

import numpy as np
import rct


if __name__ == '__main__':

    # Configure logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
    logging.getLogger('rct').setLevel(logging.DEBUG)

    tf2_publisher = rct.TransformerFactory().create_transform_publisher("ExamplePublisher")

    translation = Vector3([0., 1., 2.])
    rotation = Quaternion.from_x_rotation(np.pi)
    scale = Vector3([1., 1., 1.])
    matrix = Matrix44.from_translation(translation) * rotation

    af_s = rct.Affine3d(translation, matrix.quaternion, scale)
    t_s = rct.Transform(af_s, "A", "B", time.time())
    tf2_publisher.send_transform(t_s, rct.TransformType.STATIC)

    angle = 0
    position = Vector3([1., 0., 0.])
    while(True):

        angle += 0.01
        if angle > (2 * np.pi):
            angle = 0

        rotation = Quaternion.from_x_rotation(angle)

        af_d = rct.Affine3d(position, rotation, scale)
        t_d = rct.Transform(af_d, "B", "C", time.time())

        tf2_publisher.send_transform(t_d, rct.TransformType.DYNAMIC)
        time.sleep(.02)
