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

    time.sleep(2)

    print "\nrun 1 (right now)"
    try:
        transformation = tf2_subscriber.lookup_transform("A", "C", time.time())
        print "Success!"
        transformation.print_contents()
    except Exception, e:
        print "ERROR: ", e

    print "\nrun 2 (20 ms ago)"
    try:
        transformation = tf2_subscriber.lookup_transform("A", "C", time.time() - 0.2)
        print "Success!"
        transformation.print_contents()
    except Exception, e:
        print "ERROR: ", e

    print "\nrun 3 (1 s ago)"
    try:
        transformation = tf2_subscriber.lookup_transform("A", "C", time.time() - 1.0)
        print "Success!"
        transformation.print_contents()
    except Exception, e:
        print "ERROR: ", e
