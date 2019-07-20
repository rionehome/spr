#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from spr.msg import Activate


class PersonRecognition:
    def __init__(self):
        rospy.Subscriber("/spr/activate/0", Activate, activate_callback)
    
    def test_callback(self, msg):
        print msg


def activate_callback(msg):
    print msg
    person = PersonRecognition()
    rospy.spin()


if __name__ == '__main__':
    rospy.init_node("activate")
    rospy.spin()
