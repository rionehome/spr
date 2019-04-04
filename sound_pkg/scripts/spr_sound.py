#!/usr/bin/env python
#! -*- coding:utf8 -*-
import math
import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech,get_model_path
import os
import socket
dammy = os.path.abspath("spr_sound.py")
pre = dammy.strip("/scripts/spr_sound.py")

kw_path = '/'+pre+'/dictionary/rosquestion.list'
es_path = '/'+pre+'/dictionary/espeak.list'
dc_path = '/'+pre+'/dictionary/rosquestion.dict'

text = 'start game'#if you want to change start sign, change this text.


def recognize_sign(): 

    while True:
        speech = LiveSpeech(lm=False, keyphrase='start game', kws_threshold=1e-20)#set pocketsphinx's module
        for phrase in speech:
            sp = str(phrase)
	    if sp == text:
                break
        else:
            continue
        break

    publish_sign(text)

def publish_sign(phrase):

    os.system("espeak 'Hello, everyone, let start game'")#Speech sign

    pub = rospy.Publisher('srtcont',String,queue_size=10)#node  is srtcont which communicates with control systems.
    pub.publish('001')
    rospy.loginfo(phrase)

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
        kws = kw_path,
        hmm=os.path.join(model_path, 'en-us'),
        dic=os.path.join(model_path,dc_path)
    )

    # read question_keyword file
    with open(kw_path) as f:
        qw = [s.strip() for s in f.readlines()]
    print qw

    #read Speech phrase list file
    with open(es_path,'r') as fi:
	pl = [ki.strip() for ki in fi.readlines()]
        pl.pop()
    print pl

    for phrase in speech:
        sp = str(phrase)
        print(sp)

        for i in range(0,6):
       	    if sp == qw[i]:
                os.system("espeak '{}'".format(pl[i]))

def callback(data):
    if data.data == "003":
    #if data.data == "001":
        os.system("espeak 'detect faces'")
	rospy.signal_shutdown("recognize_question")
def calc_cos(list1,list2):
    sum = 0
    for word in list1:
        if word in list2:
            sum += 1
    v1 = math.sqrt(list1)
    v2 = math.sqrt(list2)
    return sum/(v1*v2)
def get_angle():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('127.0.0.1', 50007))
    while True:
        data = s.recv(1024)# the type of data is string
        return data
def listener():
    rospy.Subscriber("/srtqeus",String,callback)
    #rospy.Subscriber('/srtcont',String,queue_size=10)
    rospy.spin()
if __name__ == '__main__':
    rospy.init_node('talker')
    #recognize_sign()
    #listener()
    recognize_question()
