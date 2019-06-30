#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import rospy
from sound_system.srv import StringService
from start_pkg.msg import Activate
from std_msgs.msg import String
import os


class RiddleGameSPR:
    def __init__(self, activate_id):
        rospy.init_node('riddle_game_spr')
        rospy.Subscriber("/spr/activate", Activate, self.activate_callback)
        
        self.activate_pub = rospy.Publisher("/spr/activate", Activate, queue_size=10)
        self.change_dict_pub = rospy.Publisher("/sound_system/sphinx/dict", String, queue_size=10)
        self.change_gram_pub = rospy.Publisher("/sound_system/sphinx/gram", String, queue_size=10)
        self.dic_path = os.path.dirname(os.path.abspath(__file__))
        self.q_a_path = self.dic_path.replace("/the_riddle_game_pkg/src", "/q&a/q&a.csv")
        self.a_q_dict = self.read_q_a(self.q_a_path)
        self.id = activate_id
        
        print self.a_q_dict
    
    def activate_callback(self, msg):
        # type:(Activate)->None
        if msg.id == self.id:
            for i in range(5):
                print i + 1
                text = self.resume_text("spr_sample_sphinx")
                print text
                if text not in self.a_q_dict:
                    continue
                answer = self.a_q_dict[text]
                print answer
                self.speak(answer)
            print "id4に送信"
            self.activate_pub.publish(Activate(id=self.id + 1))
    
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


if __name__ == '__main__':
    RiddleGameSPR(3)
    rospy.spin()
