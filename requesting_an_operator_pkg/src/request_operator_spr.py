#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import cv2
import os
import shutil
from sound_system.srv import StringService
from start_pkg.msg import Activate
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


class FaceCut:
	def __init__(self, activate_id):
		rospy.init_node('req_operator_spr')

		rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
		rospy.Subscriber("/spr/activate", Activate, self.activate_callback)

		self.activate_pub = rospy.Publisher("/spr/activate", Activate, queue_size=10)
		self.id = activate_id
		self.bridge = CvBridge()
		self.color_image = None

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

	def image_callback(self, image):
		# type: (Image)->None
		try:
			self.color_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
		except CvBridgeError:
			print "Error at CVBridge"

	def activate_callback(self, msg):
		if msg.data == self.id:
			self.face_count()
			self.activate_pub.publish(Activate(id=self.id + 1))

	def face_count(self):
		while True:
			self.speak("Count the number of people after 5 seconds.")
			r = rospy.Rate(1)
			print "wait 10 second"
			for i in range(5):
				print i + 1
				r.sleep()

			while self.color_image is None:
				print "画像待機"

			image_gray = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2GRAY)
			cascade = cv2.CascadeClassifier(face_cascade_path)
			face_rects = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(2, 2))
			print face_rects
			if len(face_rects) <= 0:
				print "顔が認識できません"
				continue

			# ファイルの削除&生成
			if os.path.exists(pre_path):
				shutil.rmtree(pre_path)
			os.mkdir(pre_path)

			for i in range(len(face_rects)):
				[x, y, w, h] = face_rects[i]
				print face_rects[i]
				img_cropped = cv2.resize(self.color_image[y:y + h, x:x + w], (96, 96))  ##パラメータ変更要
				filename = pre_path + ("/img_%02d.png" % i)
				cv2.imwrite(filename, img_cropped)
			m_count = mf.main("男女認識")
			f_count = len(face_rects) - m_count
			self.speak('There are {0} male and {1} female.'.format(m_count, f_count))
			break


if __name__ == "__main__":
	FaceCut(2)
	rospy.spin()
