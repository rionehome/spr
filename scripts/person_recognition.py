#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import rospkg
import shutil

import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image
from sound_system.srv import StringService
from spr.msg import Activate
from module import gender_predict


class PersonRecognition:
    def __init__(self, activate_id):
        self.color_image = None
        self.bridge = CvBridge()
        self.etc_path = "{}/etc/".format(rospkg.RosPack().get_path('sound_system'))
        
        rospy.init_node("person recognition")
        rospy.Subscriber("/spr/activate/{}".format(activate_id), Activate, self.activate_callback)
        rospy.Subscriber("/camera/rgb/image_raw", Image, self.color_image_callback)
        self.activate_pub = rospy.Publisher("/spr/activate/{}".format(activate_id + 1), Activate, queue_size=10)
    
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
    
    def get_face_rests(self):
        """
        color_imageから顔の四角を取得
        :return:
        """
        while True:
            __image_gray__ = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2GRAY)
            __cascade__ = cv2.CascadeClassifier(self.etc_path + "haarcascade_frontalface_default.xml")
            __face_rects__ = __cascade__.detectMultiScale(__image_gray__, scaleFactor=1.2, minNeighbors=2,
                                                          minSize=(2, 2))
            if not len(__face_rects__) == 0:
                break
        return __face_rects__
    
    def calc_count_persons(self, face_rects):
        # type:(list)->int
        """
        OpenCVで群衆の人数をカウント
        :param face_rects:
        :return:
        """
        __persons_path__ = "{}/log/persons/".format(self.etc_path)
        self.reset_dir(__persons_path__)
        for i in range(len(face_rects)):
            [x, y, w, h] = face_rects[i]
            __image__ = cv2.resize(self.color_image[y:y + h, x:x + w], (96, 96))  ##パラメータ変更要
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
        return gender_predict.GenderPredict("{}/log/persons/".format(self.etc_path)).calc_judge()
    
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
    
    ##############################################################################################
    
    def activate_callback(self, msg):
        # type:(Activate)->None
        """
        activate_idの受け取り
        :param msg:
        :return:
        """
        print msg, "@PersonRecognition"
        
        while self.color_image is None:
            print "画像待機"
        face_rects = self.get_face_rests()
        
        person_count = self.calc_count_persons(face_rects)
        gender_count = self.calc_count_gender()
        
        self.speak("There are {} people.".format(person_count))
        self.speak("There are {} male and {} female.".format(gender_count[0], gender_count[1]))
        
        self.activate_pub.publish(Activate())


if __name__ == '__main__':
    PersonRecognition(1)
    rospy.spin()
