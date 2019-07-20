#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospkg

import cv2
from cv_bridge import CvBridge, CvBridgeError
import rospy
from sensor_msgs.msg import Image
from spr.msg import Activate


class PersonRecognition:
    def __init__(self, activate_id):
        self.color_image = None
        self.bridge = CvBridge()
        
        rospy.init_node("person recognition")
        rospy.Subscriber("/spr/activate/{}".format(activate_id), Activate, self.activate_callback)
        rospy.Subscriber("/camera/rgb/image_raw", Image, self.color_image_callback)
    
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
    
    def get_face_rests(self):
        """
        color_imageから顔の四角を取得
        :return:
        """
        __face_cascade_path__ = "{}/{}".format(rospkg.RosPack().get_path('sound_system'), "etc")
        image_gray = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2GRAY)
        cascade = cv2.CascadeClassifier(__face_cascade_path__)
        face_rects = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(2, 2))
    
    def activate_callback(self, msg):
        # type:(Activate)->None
        print msg, "@PersonRecognition"
        while self.color_image is None:
            print "画像待機"


if __name__ == '__main__':
    PersonRecognition(1)
    rospy.spin()
