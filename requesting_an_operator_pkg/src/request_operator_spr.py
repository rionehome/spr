#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import cv2
import os
from std_msgs.msg import String
from sensor_msgs.msg import Image
import male_female_predict as mf
from cv_bridge import CvBridge, CvBridgeError

dic_path = os.path.dirname(os.path.abspath(__file__))
face_cascade_path = dic_path.replace("requesting_an_operator_pkg/src",
									 "requesting_an_operator_pkg/images/haarcascade_frontalface_default.xml")

jpg_path = dic_path.replace("requesting_an_operator_pkg/src",
							"requesting_an_operator_pkg/images/predict/img_crowd.jpg")
pre_path = dic_path.replace("requesting_an_operator_pkg/src",
							"requesting_an_operator_pkg/images/predict")
print face_cascade_path
ORG_WINDOW_NAME = "cap"
GAUSSIAN_WINDOW_NAME = "cap_gray"


class Face_cut:
	def __init__(self):
		rospy.init_node('req_operator_spr')
		self.pub3 = rospy.Publisher("detect_face", String, queue_size=10, latch=True)
		self.bridge = CvBridge()
		self.color_image = None
		rospy.Subscriber("face_recognize", String, self.callback)
		rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)

	def image_callback(self, image):
		# type: (Image)->None
		print "debug"
		try:
			self.color_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
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

			image_gray = cv2.cvtColor(self.color_image, cv2.COLOR_BGR2GRAY)
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
				imgCroped = cv2.resize(self.color_image[y:y + h, x:x + w], (96, 96))  ##パラメータ変更要
				filename = pre_path + ("/img_%02d.jpg" % i)
				cv2.imwrite(filename, imgCroped)
			m_count = mf.main("男女認識")
			f_count = len(facerect) - m_count
			self.pub3.publish('03')
			break


if __name__ == "__main__":
	Face_cut()
	rospy.spin()
