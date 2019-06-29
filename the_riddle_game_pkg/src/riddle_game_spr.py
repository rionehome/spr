#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import rospy
from sound_system.srv import StringService
from start_pkg.msg import Activate
from std_msgs.msg import String
import os


class RiddleGameSPR:
	def __init__(self, activate_id):
		rospy.init_node('riddle_game_spr')
		rospy.Subscriber("/spr/activate", Activate, self.activate_callback)

		self.activate_pub = rospy.Publisher("/spr/activate", Activate, queue_size=10)
		self.change_dict_pub = rospy.Publisher("/sound_system/sphinx/dict", String, queue_size=10)
		self.change_gram_pub = rospy.Publisher("/sound_system/sphinx/gram", String, queue_size=10)
		self.dic_path = os.path.dirname(os.path.abspath(__file__))
		self.q_a_path = self.dic_path.replace("/the_riddle_game_pkg/src", "/q&a/q&a.csv")
		self.a_q_dict = self.read_q_a(self.q_a_path)
		self.id = activate_id

		print self.a_q_dict

	def activate_callback(self, msg):
		if msg.data == self.id:
			for i in range(5):
				text = self.resume_text("spr_sample_sphinx")
				answer = self.a_q_dict[text]
				print answer
				self.speak(answer)

			self.activate_pub.publish(Activate(id=self.id + 1))

	@staticmethod
	def read_q_a(path):
		# type: (str)->dict
		"""
		q&aのcsvを辞書型リストに取り込む
		:param path:
		:return:
		"""
		with open(path, "r") as f:
			read_dict = csv.DictReader(f, delimiter=";", quotechar='"')
			ks = read_dict.fieldnames
			return_dict = {k: [] for k in ks}

			for row in read_dict:
				for k, v in row.items():
					return_dict[k].append(v)  # notice the type of the value is always string.

		return return_dict

	@staticmethod
	def speak(sentence):
		# type: (str) -> None
		"""
		speak関数
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


if __name__ == '__main__':
	RiddleGameSPR(3)
	rospy.spin()
