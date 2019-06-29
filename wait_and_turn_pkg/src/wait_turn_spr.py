#!/usr/bin/env python
# -*- coding: utf-8 -*-
import math
from nav_msgs.msg import Odometry
import rospy
from start_pkg.msg import Activate
from std_msgs.msg import String
from geometry_msgs.msg import Twist


class TurnSPR:
	def __init__(self, activate_id):
		rospy.init_node('turn_spr')

		rospy.Subscriber("/spr/activate", Activate, self.activate_callback)
		rospy.Subscriber('/odom', Odometry, self.now_angular)

		self.activate_pub = rospy.Publisher("/spr/activate", Activate, queue_size=10)
		self.pub02 = rospy.Publisher('face_recognize', String, queue_size=10)
		self.velocity_pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
		self.angular = 0.0
		self.id = activate_id

	def activate_callback(self, msg):
		# type: (Activate)->None
		if msg.id == self.id:
			# 180度回転
			self.turn_180()
			self.activate_pub.publish(Activate(id=self.id + 1))

	def turn_180(self):
		"""
		180度回転
		:return:
		"""
		finish_turn = False
		while not finish_turn:
			print self.angular
			vel = Twist()
			vel.linear.x = 0.0
			if - 5 < self.angular < 177:
				vel.angular.z = 0.6
				self.velocity_pub.publish(vel)
			elif -5 >= self.angular >= -177:
				vel.angular.z = -0.6
				self.velocity_pub.publish(vel)
			elif 177 <= self.angular < 179.8:
				# print "2"
				vel.angular.z = 0.3
				self.velocity_pub.publish(vel)

			elif -179.8 < self.angular < -177:
				vel.angular.z = -0.3
				self.velocity_pub.publish(vel)
			else:
				vel.angular.z = 0.0
				self.velocity_pub.publish(vel)
				finish_turn = True

	def now_angular(self, message):
		"""
		オドメトリ取得
		:param message:
		:return:
		"""
		prinentation_z = message.pose.pose.orientation.z
		self.angular = math.degrees(2 * math.asin(prinentation_z))


if __name__ == '__main__':
	TurnSPR(1)
	rospy.spin()
