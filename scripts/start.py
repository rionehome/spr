#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sound_system.srv import StringService
from spr.msg import Activate

import rospy
from std_msgs.msg import String, Float64MultiArray, Int32


class Start:
    def __init__(self, activate_id):
        rospy.init_node('start')
        rospy.Subscriber("/spr/activate/{}".format(activate_id), Activate, self.activate_callback)
        rospy.Subscriber("/move/amount/signal", Int32, self.amount_signal_callback)
        self.activate_pub = rospy.Publisher("/spr/activate/{}".format(activate_id + 1), Activate, queue_size=10)
        self.move_amount_pub = rospy.Publisher("/move/amount", Float64MultiArray, queue_size=10)
    
    def activate_callback(self, msg):
        # type: (Activate)->None
        print msg
        self.resume_start("spr_sound")
    
    def sound_recognition_callback(self, msg):
        # type:(String)->None
        """
        音声認識の結果を受け取る
        :param msg:
        :return:
        """
        if msg.data == "start game":
            self.start()
    
    def amount_signal_callback(self, data):
        # type:(Int32)->None
        if data.data == 1:
            return
        self.activate_pub.publish(Activate())
    
    def move_turn(self, angle):
        """
        角度送信
        :param angle:
        :return:
        """
        array = Float64MultiArray()
        array.data.append(0)
        array.data.append(0)
        array.data.append(angle)
        array.data.append(1)
        self.move_amount_pub.publish(array)
    
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
    
    @staticmethod
    def resume_start(dict_name):
        # type: (str)->str
        """
        音声認識
        :return:
        """
        rospy.wait_for_service("/sound_system/recognition")
        response = rospy.ServiceProxy("/sound_system/recognition", StringService)(dict_name)
        return response.response
    
    def start(self):
        self.speak("Hello, everyone, let\'s start game.")
        # 10秒待機
        r = rospy.Rate(1)
        print "wait 10 second"
        for i in range(10):
            print i + 1
            r.sleep()
        
        # 180度回転
        self.move_turn(180)
        
        # amount_signal_callbackへ->


if __name__ == '__main__':
    Start(0)
    rospy.spin()
