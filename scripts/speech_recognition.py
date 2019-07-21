#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import rospkg

from sound_system.srv import StringService
from spr.msg import Activate

import rospy
from std_msgs.msg import String, Float64MultiArray, Int32


class SpeechRecognition:
    def __init__(self, activate_id):
        rospy.init_node('speech_recognition')
        
        self.etc_path = "{}/etc/".format(rospkg.RosPack().get_path('spr'))
        self.q_a_path = self.etc_path + "question_answer/question_answer_list.csv"
        self.a_q_dict = self.read_q_a(self.q_a_path)
        self.phase_count = 0
        self.activate_flag = False
        self.sound_source_angle_list = []
        self.recognition_result = ""
        
        rospy.Subscriber("/sound_direction", Int32, self.respeaker_callback)
        rospy.Subscriber("/sound_system/result", String, self.sound_recognition_callback)
        rospy.Subscriber("/move/amount/signal", Int32, self.amount_signal_callback)
        rospy.Subscriber("/spr/activate/{}".format(activate_id), Activate, self.activate_callback)
        self.move_amount_pub = rospy.Publisher("/move/amount", Float64MultiArray, queue_size=10)
    
    def respeaker_callback(self, msg):
        # type:(Int32)->None
        """
        angle_listにスタック
        :param msg:
        :return:
        """
        angle = msg.data
        if len(self.sound_source_angle_list) > 10:
            self.sound_source_angle_list.pop(0)
        self.sound_source_angle_list.append(angle)
    
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
    
    def turn_sound_source(self):
        """
        音源定位した後の移動
        :return:
        """
        # 回転メッセージを投げる
        angle = self.sound_source_angle_list[3]  # 時間を遡る
        if angle - 180 > 0:
            angle = -(360 - angle)
        self.move_turn(angle)
    
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
        # type: (Activate)->None
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
        
        self.recognition_result = msg.data
        if self.recognition_result not in self.a_q_dict:
            print "質問リストにありませんでした。"
            self.resume_start("spr_sample_sphinx")
            return
        
        if self.phase_count < 5:
            # 音源定位なし
            print "phase:", self.phase_count
            __answer__ = self.a_q_dict[self.recognition_result]
            print __answer__
            self.speak(__answer__)
            self.phase_count += 1
            self.resume_start("spr_sample_sphinx")
        else:
            # 音源定位あり
            self.turn_sound_source()
    
    def amount_signal_callback(self, msg):
        # type:(Int32)->None
        """
        180度回転が終わったという信号を受け取る
        :param msg:
        :return:
        """
        if not self.activate_flag:
            return
        if msg.data == 1:
            return
        __answer__ = self.a_q_dict[self.recognition_result]
        print __answer__
        self.speak(__answer__)
        self.resume_start("spr_sample_sphinx")


if __name__ == '__main__':
    SpeechRecognition(2)
    rospy.spin()
