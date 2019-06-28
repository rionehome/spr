#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import sys
import cv2
import os
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
import male_female_predict as mf
from cv_bridge import CvBridge, CvBridgeError
import shutil
import time

dicpath = os.path.dirname(os.path.abspath(__file__))
face_cascade_path = dicpath.replace("requesting_an_operator_pkg/src",
									"requesting_an_operator_pkg/etc/opencv-3.3.1/data/haarcascades/haarcascade_frontalface_default.xml")

jpg_path = dicpath.replace("requesting_an_operator_pkg/src",
						   "requesting_an_operator_pkg/images/predict/img_crowd.jpg")
pre_path = dicpath.replace("requesting_an_operator_pkg/src",
						   "requesting_an_operator_pkg/images/predict")
print face_cascade_path
ORG_WINDOW_NAME = "cap"
GAUSSIAN_WINDOW_NAME = "cap_gray"


class Face_cut:
	def __init__(self):
		rospy.init_node('req_operator_spr')
		self.pub3 = rospy.Publisher("detect_face", String, queue_size=10, latch=True)
		self.bridge = CvBridge()
		self.image_org = None
		self.sub = rospy.Subscriber("face_recognize", String, self.callback)
		self.image_sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)

	def get_image(self, img):
		try:
			self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
		except CvBridgeError:
			print "Error at CVBridge"

	def callback(self, msg):
		print "callback"
		if msg.data == "02":
			print msg
			self.face_count()

	def face_count(self):
		while True:
			print "wait 10 munites"
			rospy.sleep(10)

			while self.image_org is None:
				rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)

			image_gray = cv2.cvtColor(self.image_org, cv2.COLOR_BGR2GRAY)
			cascade = cv2.CascadeClassifier(face_cascade_path)
			facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(2, 2))
			print facerect
			if len(facerect) <= 0:
				print "顔が認識できません"
				continue

			if os.path.exists(pre_path) == False:
				os.mkdir(pre_path)

			for i in range(len(facerect)):
				[x, y, w, h] = facerect[i]
				print facerect[i]
				imgCroped = cv2.resize(self.image_org[y:y + h, x:x + w], (96, 96))  ##パラメータ変更要
				filename = pre_path + ("/img_%02d.jpg" % i)
				cv2.imwrite(filename, imgCroped)
			m_count = mf.main("男女認識")
			f_count = len(facerect) - m_count
			self.pub3.publish('03')
			break


if __name__ == "__main__":
	Face_cut()
	rospy.spin()
