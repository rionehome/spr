#!/usr/bin/env python
# -*- coding: utf-8 -*-
import actionlib
from sound_system.srv import StringService
import rospy
from std_msgs.msg import String
from move.msg import AmountAction, AmountGoal


class BeginningGame:
    def __init__(self, activate_id):
        rospy.init_node('start')
        
        self.activate_flag = False
        
        rospy.Subscriber("/spr/activate/{}".format(activate_id), String, self.activate_callback)
        rospy.Subscriber("/sound_system/result", String, self.sound_recognition_callback)
        self.activate_pub = rospy.Publisher("/spr/activate/{}".format(activate_id + 1), String, queue_size=10)
        self.client = actionlib.SimpleActionClient("/move/amount", AmountAction)
    
    def move_turn(self, angle):
        """
        角度送信
        :param angle:
        :return:
        """
        goal = AmountGoal()
        goal.amount.angle = angle
        goal.velocity.angular_rate = 0.5
        
        self.client.wait_for_server()
        self.client.send_goal(goal)
        self.client.wait_for_result(rospy.Duration(10))
    
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
    
    #########################################################################################################
    
    def activate_callback(self, msg):
        # type: (String)->None
        self.activate_flag = True
        print msg, "@BeginningGame"
        # 音声認識スタート
        print "Please say \"start game\"."
        self.resume_start("spr_sound")
    
    def sound_recognition_callback(self, msg):
        # type:(String)->None
        """
        音声認識の結果を受け取る
        :param msg:
        :return:
        """
        if not self.activate_flag:
            return
        
        if msg.data == "start game":
            self.speak("Hello, everyone, let\'s start game.")
            # 10秒待機
            r = rospy.Rate(1)
            print "wait 10 second"
            for i in range(10):
                print i + 1
                r.sleep()
            
            # 180度回転
            self.move_turn(180)
            
            self.activate_pub.publish(String())
            self.activate_flag = False


if __name__ == '__main__':
    BeginningGame(0)
    rospy.spin()
