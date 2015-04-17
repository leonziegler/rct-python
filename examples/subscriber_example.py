#!/usr/bin/python
# Imports
import logging
import time
import rct


if __name__ == '__main__':
    print "starting"

    # Configure logging
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
    logging.getLogger('rsb').setLevel(logging.ERROR)
    logging.getLogger('rct').setLevel(logging.INFO)

    tf2_subscriber = rct.TransformerFactory().create_transform_receiver()

    print "run 1"
    try:
        transformation = tf2_subscriber.lookup_transform("A", "C", time.time())
        transformation.print_contents()
    except Exception, e:
        print "ERROR: ", e

    print "run 2"
    try:
        transformation = tf2_subscriber.lookup_transform("A", "C", time.time())
        transformation.print_contents()
    except Exception, e:
        print "ERROR: ", e

    print "run 3"
    try:
        transformation = tf2_subscriber.lookup_transform("A", "C", time.time() - 0.2)
        transformation.print_contents()
    except Exception, e:
        print "ERROR: ", e
