#!/usr/bin/env python
# -*- coding: utf-8 -*-
from kobuki_msgs.msg import ButtonEvent
import rospy
from std_msgs.msg import String


class Trigger:
    def __init__(self):
        rospy.init_node("trigger")
        rospy.Subscriber("/mobile_base/events/button", ButtonEvent, self.kobuki_button_callback)
        self.activate_pub = rospy.Publisher("/spr/activate/0", String, queue_size=10)
    
    def kobuki_button_callback(self, msg):
        # type:(ButtonEvent)->None
        """
        kobukiのボタン0の入力を受け取り
        :param msg:
        :return:
        """
        print msg, "@Trigger"
        if msg.button == 0 and msg.state == 1:
            self.activate_pub.publish(String())


if __name__ == '__main__':
    Trigger()
    rospy.spin()
