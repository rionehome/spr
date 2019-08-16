#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import os
import rospkg
import shutil
import sys

import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image
from sound_system.srv import StringService
from std_msgs.msg import String
from tfpose_ros.msg import Poses
from module import se

from module import gender_predict


class PersonRecognition:
    def __init__(self, activate_id):
        rospy.init_node("person recognition")
        
        self.color_image = None
        self.take_color_image = None
        self.bridge = CvBridge()
        self.se = se.SE()
        self.etc_path = "{}/etc/".format(rospkg.RosPack().get_path('spr'))
        self.point_list = ["nose", "leftEye", "rightEye", "leftEar", "rightEar"]
        
        rospy.Subscriber("/spr/activate/{}".format(activate_id), String, self.activate_callback)
        rospy.Subscriber("/camera/color/image_raw", Image, self.color_image_callback)
        # rospy.Subscriber("/usb_cam/image_raw", Image, self.color_image_callback)
        rospy.Subscriber("/tfpose_ros/output", Poses, self.poses_callback, queue_size=1)
        self.activate_pub = rospy.Publisher("/spr/activate/{}".format(activate_id + 1), String, queue_size=10)
        self.image_pub = rospy.Publisher("/tfpose_ros/input", Image, queue_size=1)
    
    @staticmethod
    def reset_dir(dir_path):
        # type:(str)->None
        """
        ディレクトリのリセット
        :param dir_path:
        :return:
        """
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        os.mkdir(dir_path)
    
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
    
    def get_face_rects(self, msg):
        # type:(Poses)->list
        """
        pose情報から顔を切り取り
        :param msg:
        :return:
        """
        rects = []
        for pose in msg.poses:
            min_point = (sys.float_info.max, sys.float_info.max)
            max_point = (0.0, 0.0)
            center = (-1.0, -1.0)
            for key in pose.keypoints:
                print key.score
                key_image_x = key.image_position.x
                key_image_y = key.image_position.y
                if key.part in self.point_list:
                    if min_point[0] > key_image_x:
                        min_point = (key_image_x, key_image_y)
                    if max_point[0] < key_image_x:
                        max_point = (key_image_x, key_image_y)
                if key.part == "nose":
                    center = (key_image_x, key_image_y)
            
            # 鼻が認識していない場合
            if center[1] == -1:
                center = ((min_point[0] + max_point[0]) / 2, (min_point[1] + max_point[1]) / 2)
            
            if int(max_point[0] - min_point[0]) == 11:
                rects = []
                return rects
            
            x = int(min_point[0])
            y = int(center[1] - ((max_point[0] - min_point[0]) / 2))
            w = int(max_point[0] - min_point[0])
            h = int(max_point[0] - min_point[0])
            
            if w == 0 or h == 0:
                continue
            
            rects.append([x, y, w, h])
        return rects
    
    def calc_count_persons(self, face_rects):
        # type:(list)->int
        """
        OpenCVで群衆の人数をカウント
        :param face_rects:
        :return:
        """
        __persons_path__ = self.etc_path + "log/persons/"
        self.reset_dir(__persons_path__)
        for i in range(len(face_rects)):
            [x, y, w, h] = face_rects[i]
            __image__ = cv2.resize(self.take_color_image[y:y + h, x:x + w], (96, 96))  # パラメータ変更要
            __file_name__ = __persons_path__ + ("img_%02d.png" % i)
            cv2.imwrite(__file_name__, __image__)
        return len(face_rects)
    
    def calc_count_gender(self):
        """
        男女識別
        :return: (male,female)
        """
        self.reset_dir("males")
        self.reset_dir("females")
        return gender_predict.GenderPredict(self.etc_path + "log/persons/").calc_judge()
    
    def color_image_callback(self, msg):
        # type:(Image)->None
        """
        センサーからのカラー画像を受け取る
        :return:
        """
        try:
            self.color_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except CvBridgeError:
            print "Error at CVBridge"
    
    def wait_image_and_publish(self):
        while self.color_image is None:
            print "画像待機"
        self.take_color_image = copy.deepcopy(self.color_image)
        self.image_pub.publish(self.bridge.cv2_to_imgmsg(self.take_color_image, encoding="bgr8"))
    
    ##############################################################################################
    
    def activate_callback(self, msg):
        # type:(String)->None
        """
        activate_idの受け取り
        :param msg:
        :return:
        """
        print msg, "@PersonRecognition"
        
        self.wait_image_and_publish()
        self.se.play(self.se.SHUTTER)
        self.speak("Now analyzing...")
    
    def poses_callback(self, msg):
        # type:(Poses)->None
        face_rects = self.get_face_rects(msg)
        if len(face_rects) == 0:
            self.speak("sorry, one more time.")
            self.wait_image_and_publish()
            self.se.play(self.se.SHUTTER)
            self.speak("Now analyzing...")
            return
        print face_rects
        person_count = self.calc_count_persons(face_rects)
        gender_count = self.calc_count_gender()
        
        self.speak("There are {} people.".format(person_count))
        self.speak("There are {} male and {} female.".format(gender_count[0], gender_count[1]))
        
        self.activate_pub.publish(String())


if __name__ == '__main__':
    PersonRecognition(1)
    rospy.spin()
