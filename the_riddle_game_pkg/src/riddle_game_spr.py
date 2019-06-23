#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import math
import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
import os
import socket
dicpath = os.path.dirname(os.path.abspath(__file__))
kw_path = dicpath.replace("/the_riddle_game_pkg/src","/the_riddle_game_pkg/dictionary/rosquestion.list")
es_path = dicpath.replace("/the_riddle_game_pkg/src","/the_riddle_game_pkg/dictionary/espeak.list")
dc_path = dicpath.replace("/the_riddle_game_pkg/src","/the_riddle_game_pkg/dictionary/rosquestion.dict")
flag = False

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
	sub03 = rospy.wait_for_message('detect_face', String)	
	if sub03 == '03':
		print "recognize_question()"
		recognize_question()
		pub04 = rospy.Publisher('sound_localization', String, queue_size=10)
		rospy.sleep(2)
		pub04.publish('04')
	rospy.spin()
