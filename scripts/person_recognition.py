#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from spr.msg import Activate


class PersonRecognition:
    def __init__(self, activate_id):
        rospy.Subscriber("/spr/activate/{}".format(activate_id), Activate, self.activate_callback)
    
    def activate_callback(self, msg):
        # type:(Activate)->None
        
        pass


if __name__ == '__main__':
    PersonRecognition(1)
    rospy.spin()
