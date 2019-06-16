#!/usr/bin/env python
# ! -*- coding:utf-8 -*-
import sys

import math
import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
import os
import socket

dammy = os.path.abspath('riddle_game_spr.py')
pre = dammy.strip("riddle_game_spr.py")
kw_path = '/' + pre + '/dictionary/rosquestion.list'
es_path = '/' + pre + '/dictionary/espeak.list'
dc_path = '/' + pre + '/dictionary/rosquestion.dict'


def recognize_question():
	model_path = get_model_path()
	speech = LiveSpeech(
		verbose=False,
		sampling_rate=16000,
		buffer_size=2048,
		no_search=False,
		full_utt=False,
		lm=False,
		kws_threshold=1e-20,
		kws=kw_path,
		hmm=os.path.join(model_path, 'en-us'),
		dic=os.path.join(model_path, dc_path)
	)

	# read Question_keyword file
	with open(kw_path) as f:
		qw = [s.strip() for s in f.readlines()]
	print qw

	# read Speech phrase list file
	with open(es_path) as fi:
		pl = [ki.strip() for ki in fi.readline()]
		pl.pop()
	print pl

	for phrase in speech:
		sp = str(phrase)
		print(sp)
		for i in range(0, 6):
			if sp == qw[i]:
				os.system("espeak '{}'".format(pl[i]))


def callback(data):
	if data.data == '03':
		os.system("espeak 'detect faces'")
		recognize_question()
		pub04 = rospy.Publisher('sound_localization', String, queue_size=10)
		pub04.publish('04')
		sys.exit()


def calc_cos(list1, list2):
	sum = 0
	for word in list1:
		if word in list2:
			sum += 1
	v1 = math.sqrt(list1)
	v2 = math.sqrt(list2)
	return sum / (v1 * v2)


if __name__ == '__main__':
	rospy.init_node('riddle_game_spr')
	sub03 = rospy.Subscriber('detect_face', String, callback)
	rospy.spin()
