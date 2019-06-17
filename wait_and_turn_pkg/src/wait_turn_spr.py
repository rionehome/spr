#!/usr/bin/env python
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
		vel.angular.z = 1.0
		if not finish_turn:
			pub_A1.publish(vel)
	# print "1."
	elif angular >= 177 and angular < 179.8:
		# print "2"
		vel.angular.z = 0.3
		if not finish_turn:
			pub_A1.publish(vel)
	# print "2."
	else:
		vel.angular.z = 0.0
		if not finish_turn:
			pub_A1.publish(vel)
		pub02 = rospy.Publisher('face_recognize', String, queue_size=10)
		time.sleep(1)
		pub02.publish('02')
		finish_turn = True


# print "3."


def listener():
	print "listener"
	rospy.init_node('wait_turn_spr')
	rospy.Subscriber('Turn_180', String, callback)
	rospy.Subscriber('/odom', Odometry, NowAngular)
	rospy.spin()


def callback(data):
	print "callback"
	if data.data == '01':
		odom = Odometry()
		while not rospy.is_shutdown():
			Turn_180()
		print("Turn 180 degree.")


if __name__ == '__main__':
	listener()
