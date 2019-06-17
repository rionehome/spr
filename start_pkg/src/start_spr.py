#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
import time

import rospy
import sys
import math
import os
import socket
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
from nav_msgs.msg import Odometry
dicpath = os.path.dirname(os.path.abspath(__file__))
pre_path = dicpath.strip("/src")
model_path = get_model_path()
text = 'start game'  # if you want to change start sign, change this text.

def recognize_sign():
	while True:
		speech = LiveSpeech(
			verbose=False,
			sampling_rate=16000,
			buffer_size=2048,
			no_search=False,
			full_utt=False,
			hmm=os.path.join(model_path, 'en-us'),
			lm=False,
			dic="/"+pre_path+"/dictionary/spr_sound.dict",
			jsgf="/"+pre_path+"/dictionary/spr_sound.gram"
		)

		for phrase in speech:
			wording = str(phrase)
			if wording == text:
				break
		else:
			continue
		break
	publish_sign(text)


def publish_sign(phrase):
	os.system('espeak "Hello, everyone, let\'s start game"')
	r = rospy.Rate(10)
	pub01 = rospy.Publisher('Turn_180', String, queue_size=10)
	time.sleep(1)
	pub01.publish('01')
	r.sleep()
	rospy.loginfo(phrase)


if __name__ == '__main__':
	rospy.init_node('start_spr')
	print "start"
	recognize_sign()
	rospy.spin()
