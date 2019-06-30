#!/usr/bin/env python
# ! -*- coding:utf8 -*-
import csv

import rospy
from sound_system.srv import StringService
from start_pkg.msg import Activate
from std_msgs.msg import String, Int32, Float64MultiArray
import os


class SoundLocalizationSPR:
    def __init__(self, activate_id):
        rospy.init_node('sound_localization_spr')
        rospy.Subscriber("/spr/activate", Activate, self.activate_callback)
        rospy.Subscriber("/sound_direction", Int32, self.respeaker_callback)
        rospy.Subscriber("/move/amount/signal", Int32, self.amount_signal_callback)
        self.change_dict_pub = rospy.Publisher("/sound_system/sphinx/dict", String, queue_size=10)
        self.change_gram_pub = rospy.Publisher("/sound_system/sphinx/gram", String, queue_size=10)
        self.move_amount_pub = rospy.Publisher("/move/amount", Float64MultiArray, queue_size=10)
        self.move_velocity_pub = rospy.Publisher("/move/velocity", Float64MultiArray, queue_size=10)
        self.dic_path = os.path.dirname(os.path.abspath(__file__))
        self.q_a_path = self.dic_path.replace("/sound_source_localization_pkg/src", "/q&a/q&a.csv")
        self.a_q_dict = self.read_q_a(self.q_a_path)
        self.id = activate_id
        self.angle_list = []
        self.move_flag = False
        
        print self.a_q_dict
    
    def activate_callback(self, msg):
        # type:(Activate)->None
        if msg.id == self.id:
            while True:
                text = self.resume_text("spr_sample_sphinx")
                print text
                if text not in self.a_q_dict:
                    continue
                answer = self.a_q_dict[text]
                print answer
                self.turn_sound_source()  # 回転
                self.move_flag = True
                while self.move_flag:
                    pass
                self.speak(answer)
    
    def amount_signal_callback(self, data):
        # type:(Int32)->None
        if data.data == 1:
            return
        self.move_flag = False
        array = Float64MultiArray()
        array.data.append(0)
        array.data.append(0)
        array.data.append(0)
        self.move_velocity_pub.publish(array)
    
    def respeaker_callback(self, data):
        # type:(Int32)->None
        """
        angle_listにスタック
        :param data:
        :return:
        """
        angle = data.data
        if len(self.angle_list) > 10:
            self.angle_list.pop(0)
        self.angle_list.append(angle)
    
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
        speak関数
        :param sentence:
        :return:
        """
        rospy.wait_for_service("/sound_system/speak")
        rospy.ServiceProxy("/sound_system/speak", StringService)(sentence)
    
    def resume_text(self, dict_name):
        # type: (str)->str
        """
        音声認識
        :return:
        """
        self.change_dict_pub.publish(dict_name + ".dict")
        self.change_gram_pub.publish(dict_name + ".gram")
        rospy.wait_for_service("/sound_system/recognition")
        response = rospy.ServiceProxy("/sound_system/recognition", StringService)()
        return response.response
    
    def pub_move_angle(self, angle):
        """
        角度のみ送信
        :param angle:
        :return:
        """
        array = Float64MultiArray()
        array.data.append(0)
        array.data.append(0)
        array.data.append(angle)
        array.data.append(1)
        self.move_amount_pub.publish(array)
    
    def turn_sound_source(self):
        """
        音源定位した後の移動
        :return:
        """
        # 回転メッセージを投げる
        angle = self.angle_list[3]  # 時間を遡る
        if angle - 180 > 0:
            angle = -(360 - angle)
        self.pub_move_angle(angle)
        self.move_flag = True


if __name__ == '__main__':
    SoundLocalizationSPR(4)
    rospy.spin()
