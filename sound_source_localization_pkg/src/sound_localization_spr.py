#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
import sys
import socket
import getting_array as ga


def sound_localization(degree):
	pub_A2 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	vel = Twist()
	vel.linear.x = 0.0
	if degree > 180.0:
		vel.angular.z = 1.0
		degree = (degree - 360.0) * -1
		turn_time = (degree * 0.159155) // 57.29578
		for i in range(turn_time):
			pub_A2.publish(vel)
	else:
		vel.angular.z = -1.0
		turn_time = (degree - 0.159155) // 57.29578
		for i in range(turn_time):
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
