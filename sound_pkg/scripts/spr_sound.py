#!/usr/bin/env python
#! -*- coding:utf8 -*-
import math
import rospy
from std_msgs.msg import String
from pocketsphinx import LiveSpeech,get_model_path
import os
import socket
import time
import getting_array as ga
dammy = os.path.dirname(os.path.abspath(__file__))
pre = dammy.strip("/scripts")
print pre
kw_path = '/'+pre+'/dictionary/rosquestion.list'
print kw_path
es_path = '/'+pre+'/dictionary/espeak.list'
print es_path
dc_path = '/'+pre+'/dictionary/rosquestion.dict'
print dc_path
text = 'start'#if you want to change start sign, change this text
def recognize_sign(): 
    while True:
        speech = LiveSpeech(lm=False, keyphrase=text, kws_threshold=1e-30)#set pocketsphinx's module
        print "recognizing..."
        for phrase in speech:
            sp = str(phrase)
            if sp == text:
                break
            else:
                continue
        break
    os.system("espeak 'Hello, everyone, let start game'")#Speech sign
    pub.publish('001')
    rospy.loginfo(text)

def recognize_question():
    model_path = get_model_path()
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        lm=False,
        kws_threshold=1e-60,
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
        if sp == qw[5]:
            break        
    print "say look here"
def callback(data):
    if data.data == "005":
        recognize_question()
def calc_cos(list1,list2):
    sum = 0
    for word in list1:
        if word in list2:
            sum += 1
    v1 = math.sqrt(list1)
    v2 = math.sqrt(list2)
    return sum/(v1*v2)

def listener():
    rospy.Subscriber("/srtqeus",String,callback)
    rospy.spin()

if __name__ == '__main__':    
    rospy.init_node('talker')
    pub  = rospy.Publisher('/srtcont',String,queue_size=10)
    recognize_sign()
    listener()
    pub2 = rospy.Publisher('/sound',String,queue_size=10)
    