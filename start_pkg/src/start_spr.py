#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sound_system.srv import StringService
from start_pkg.msg import Activate

import rospy
from std_msgs.msg import String


class StartSPR:
	def __init__(self, activate_id):
		rospy.init_node('start_spr')

		rospy.Subscriber("/spr/activate", Activate, self.activate_callback)

		self.activate_pub = rospy.Publisher("/spr/activate", Activate, queue_size=10)
		self.change_dict_pub = rospy.Publisher("/sound_system/sphinx/dict", String, queue_size=10)
		self.change_gram_pub = rospy.Publisher("/sound_system/sphinx/gram", String, queue_size=10)

		self.id = activate_id

		print "start"

	@staticmethod
	def speak(sentence):
		# type: (str) -> None
		"""
		発話関数
		:param sentence:
		:return:
		"""
		rospy.wait_for_service("/sound_system/speak")
		rospy.ServiceProxy("/sound_system/speak", StringService)(sentence)

	def resume_text(self, dict_name):
		# type: (str)->str
		"""
		音声認識
		:return:
		"""
		self.change_dict_pub.publish(dict_name + ".dict")
		self.change_gram_pub.publish(dict_name + ".gram")
		rospy.wait_for_service("/sound_system/recognition")
		response = rospy.ServiceProxy("/sound_system/recognition", StringService)()
		return response.response

	def activate_callback(self, msg):
		# type: (Activate)->None
		if msg.id == self.id:
			self.start()

	def start(self):

		# "start game"認識
		while True:
			text = self.resume_text("spr_sound")
			if text == "start game":
				break

		self.speak("Hello, everyone, let\'s start game")

		# 10秒待機
		r = rospy.Rate(1)
		print "wait 10 second"
		for i in range(10):
			print i + 1
			r.sleep()
		activate = Activate()
		activate.id = 1
		self.activate_pub.publish(activate)


if __name__ == '__main__':
	StartSPR(0)
	rospy.spin()
