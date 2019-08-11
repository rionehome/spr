#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import rospkg

from sound_system.srv import StringService

import rospy
from std_msgs.msg import String


class SpeechRecognition:
    def __init__(self, activate_id):
        rospy.init_node('speech_recognition')
        
        self.etc_path = "{}/etc/".format(rospkg.RosPack().get_path('spr'))
        self.q_a_path = self.etc_path + "question_answer/question_answer_list.csv"
        self.q_a_dict = self.read_q_a(self.q_a_path)
        self.activate_flag = False
        self.count = 0
        
        rospy.Subscriber("/sound_system/result", String, self.sound_recognition_callback)
        rospy.Subscriber("/spr/activate/{}".format(activate_id), String, self.activate_callback)
        self.activate_pub = rospy.Publisher("/spr/activate/{}".format(activate_id + 1), String, queue_size=10)
    
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
    
    @staticmethod
    def read_q_a(path):
        # type: (str)->dict
        """
        q&aのcsvを辞書型リストに取り込む
        :param path:
        :return:
        """
        return_dict = {}
        with open(path, "r") as f:
            for line in csv.reader(f):
                return_dict.setdefault(str(line[0]), str(line[1]))
        
        return return_dict
    
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
    
    #########################################################################################################
    
    def activate_callback(self, msg):
        # type: (String)->None
        """
        activate_id受け取り
        :param msg:
        :return:
        """
        self.activate_flag = True
        print msg, "@SpeechRecognition"
        # 音声認識スタート
        self.resume_start("spr_sample_sphinx")
    
    def sound_recognition_callback(self, msg):
        # type:(String)->None
        """
        音声認識の結果を受け取る
        :param msg:
        :return:
        """
        if not self.activate_flag:
            return
        
        __recognition_result__ = msg.data
        if __recognition_result__ not in self.q_a_dict:
            print "質問リストにありませんでした。"
            self.resume_start("spr_sample_sphinx")
            return
        
        __answer__ = self.q_a_dict[__recognition_result__]
        print __answer__
        self.speak(__answer__)
        self.resume_start("spr_sample_sphinx")
        self.count += 1
        
        if self.count >= 5:
            self.activate_pub.publish(String())
            self.activate_flag = False
            return


if __name__ == '__main__':
    SpeechRecognition(2)
    rospy.spin()
