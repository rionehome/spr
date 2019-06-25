#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
import time
from nav_msgs.msg import Odometry
import rospy
import sys
from std_msgs.msg import String
from geometry_msgs.msg import Twist
angular = 0.0
finish_turn = False

def NowAngular(message):
	global angular
	prinentation_z = message.pose.pose.orientation.z
	angular = math.degrees(2 * math.asin(prinentation_z))


def Turn_180():
	global finish_turn
	# print "A"
	pub_A1 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
	# print angular
	vel = Twist()
	vel.linear.x = 0.0
	if angular > - 179.5 and angular < 177:
		# print "1"
		vel.angular.z = 0.6
		pub_A1.publish(vel)
	# print "1."
	elif angular >= 177 and angular < 179.8:
		# print "2"
		vel.angular.z = 0.3
		pub_A1.publish(vel)
	# print "2."
	else:
		vel.angular.z = 0.0
		pub_A1.publish(vel)
		finish_turn = True


def listener():
	print "listener"
	rospy.init_node('wait_turn_spr')
	rospy.Subscriber('Turn_180', String, callback)
	rospy.Subscriber('/odom', Odometry, NowAngular)
	rospy.spin()


def callback(data):
	print "callback"
	pub02 = rospy.Publisher('face_recognize', String, queue_size=10)
	if data.data == '01':
		print "wait 10 second"
		rospy.sleep(10)
		odom = Odometry()
		while not rospy.is_shutdown():
			Turn_180()
			if finish_turn is True:
				break

		print("Turn 180 degree.")
		rospy.sleep(2)
		rospy.loginfo(pub02)
		pub02.publish("02")

if __name__ == '__main__':
	listener()
