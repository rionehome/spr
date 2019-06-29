#!/usr/bin/env python
# ! -*- coding:utf8 -*-
import math
import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
import os

import getting_array as ga

#dammy = os.path.abspath("spr_sound.py")
#pre = dammy.strip("/scripts/spr_sound.py")
#kw_path = '/' + pre + '/dictionary/rosquestion.list'
#es_path = '/' + pre + '/dictionary/espeak.list'
#dc_path = '/' + pre + '/dictionary/rosquestion.dict'

#text = 'start game'  # if you want to change start sign, change this text.




def recognize_sign():
	while True:
		speech = LiveSpeech(lm=False, keyphrase='start game', kws_threshold=1e-20)  # set pocketsphinx's module
		for phrase in speech:
			sp = str(phrase)
			if sp == text:
				break
		else:
			continue
		break

	publish_sign(text)


def publish_sign(phrase):
	os.system("espeak 'Hello, everyone, let start game'")  # Speech sign

	pub = rospy.Publisher('srtcont', String, queue_size=10)  # node  is srtcont which communicates with control systems.
	pub.publish('001')
	rospy.loginfo(phrase)



def recognize_question():
	#model_path = get_model_path()
	"""
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
	"""
	model_path = '/usr/local/lib/python2.7/dist-packages/pocketsphinx/model'
	dic_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dictionary')
	speech = LiveSpeech(
		verbose=False,
		sampling_rate=16000,
		buffer_size=2048,
		no_search=False,
		full_utt=False,
		hmm=os.path.join(model_path, 'en-us'),
		lm=False,
		dic=os.path.join(dic_path, 'spr_sample_sphinx.dict'),
		jsgf=os.path.join(dic_path, "spr_sample_sphinx.gram")
	)

	""""
	# read question_keyword file
	with open(kw_path) as f:
		qw = [s.strip() for s in f.readlines()]
	print qw

	# read Speech phrase list file
	with open(es_path, 'r') as fi:
		pl = [ki.strip() for ki in fi.readlines()]
		pl.pop()
	print pl
	"""
	csv_file = os.path.join(dic_path, "question_sample.csv")
	qa_dic = {}
	with open(csv_file) as f:
		for line in f:
			line = line.rstrip("\n")
			qa_list = line.split(";")
			qa_dic[qa_list[0]] = qa_list[1] # 辞書のキーに問題、値に答えを格納

	for phrase in speech:
		sp = str(phrase)
		print(sp)
		if sp in qa_dic:
			os.system("espeak '{}'".format(qa_dic[sp]))

	"""
		for i in range(0, 6):
			if sp == qw[i]:
				os.system("espeak '{}'".format(pl[i]))
	"""

signal = False

def callback(data):

	global signal
	if data.data == "003":
		os.system("espeak 'detect faces'")
		get_angle()
	if data.data == "005":
		#recognize_question()
		signal = True
	rospy.signal_shutdown("recognize_question")

def sphinx_wait():
	global signal
	while 1:
		if signal == True:
			recognize_question()
			break


def calc_cos(list1, list2):
	sum = 0
	for word in list1:
		if word in list2:
			sum += 1
	v1 = math.sqrt(list1)  # type: float
	v2 = math.sqrt(list2)  # type: float
	return sum / (v1 * v2)


def get_angle():
	text = ga.get_array()
	print text


def listener():
	rospy.Subscriber("/srtqeus", String, callback)
	rospy.Subscriber("/srtga", String, callback)
	sphinx_wait()
	rospy.spin()


if __name__ == '__main__':
	rospy.init_node('talker')
	listener()
	#get_angle()
