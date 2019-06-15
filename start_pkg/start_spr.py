#!/usr/bin/env python
#! -*- coding:utf-8 -*-
import rospy
import sys
import math
import os
import socket
from std_msgs.msg import String
from pocketsphinx import LiveSpeech, get_model_path
from nav_msgs.msg import Odometry


text = 'start game' #if you want to change start sign, change this text.
angular = 0.0 


def NowAngular(message):
    global angular
    prinentation_z = message.pose.pose.orientation.z
    angular = math.degrees(2 * math.asin(prinentation_z))


def recognize_sign():
    while True:
        speech = LiveSpeech(
            lm=False, 
            keyphrase=text,
            kws_threshold=1e-40
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
    r.sleep()
    pub01 = rospy.Publisher('Turn_180',String, queue_size=10)
    pub01.publish('01')
    rospy.loginfo(phrase)


if __name__ == '__main__':
    rospy.init_node('start_spr')
    odom_sub = rospy.Subscriber('/odom', Odometry, NowAngular)
    recognize_sign()
    rospy.spin()
