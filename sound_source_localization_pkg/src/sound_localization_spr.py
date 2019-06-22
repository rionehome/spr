#!/usr/bin/env python
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from nav_msgs.msg import Odometry
import sys
import socket
import getting_array as ga


def NowAngular(message):
    global angular
    prinentation_z = message.pose.pose.orientation.z
    angular = math.degrees(2 * math.asin(prinentation_z))


def sound_localization(degree):
    pub_A2 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = 0.0
    if angular < 0:
        act_degree = angular + 360
    else:
        act_degree = angular
    head_deg = act_degree + degree #Angle to head in Odometry
    if head_deg > 360:
        head_deg = head_deg - 360
    else:
        pass
    if head_deg < 180:
        vel.angular.z = -0.5
    else:
        vel.angular.z = 0.5
    head_p = head_deg + 3.0
    head_m = head_deg - 3.0
    while head_p < act_degree and head_m >act_degree:
        if angular < 0:
            act_degree = angular + 360
        else:
            act_degree = angular
        pub_A2.publish(vel)


def get_angle():
	text = ga.get_array()
	deg = float(text)
	sound_localization(deg)
	r = rospy.Rate(150)
	r.sleep()


def callback(data):
	if data.data == '04':
		get_angle()


if __name__ == '__main__':
	rospy.init_node('sound_localization')
	sub04 = rospy.Subscriber('sound_localization', String, callback)
	rospy.spin()
