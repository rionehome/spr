#!/usr/bin/env python

import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import sys
import socket
import getting_array as ga
angular=0.0

def NowAngular(message):
    global angular
    prinentation_z = message.pose.pose.orientation.z
    angular = math.degrees(2 * math.asin(prinentation_z))


def sound_localization(angle):
    finish_turn = False
    pub_A2 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    rospy.sleep(1)
    vel = Twist()
    vel.linear.x = 0
    while finish_turn is False:
        if angular > 0 and angular < angle-3:
            vel.angular.z = 0.6
            pub_A2.publish(vel)
        elif angular <= 0 and angular >= angle -357:
            vel.angular.z = -0.6
            pub_A2.publish(vel)
        elif angular >=angle-3 and angular < angle -0.3:
            vel.angular.z = 0.3
            pub_A2.publish(vel)
        elif angular > angle -360+0.3 and angular < angle -360+0.3:
            vel.angular.z =-0.3
            pub_A2.publish(vel)
        else:
            vel.angular.z= 0
            pub_A2.publish(vel)
            finish_turn = True

def get_angle(msg):
    text = ga.get_array(msg)
    angle = float(text)
    return angle

if __name__ == '__main__':
    rospy.init_node('sound_localization')
    sub04 = rospy.wait_for_message('sound_localization', String)
    if sub04.data == '04':
        print "get message"
        angle = get_angle("look here")
        sound_localization(angle)
        print "Are you talking?"
        os.system("espeak 'Are you talking?'")

    else:
        print "message error"
