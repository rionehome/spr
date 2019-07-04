#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
import sys
import time

import rospy
import cv2
import os
import shutil
import numpy as np
from sound_system.srv import StringService
from start_pkg.msg import Activate
from sensor_msgs.msg import Image
from tfpose_ros.msg import Persons, Person, BodyPartElm

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

		# rospy.Subscriber("/camera/rgb/image_raw", Image, self.image_callback)
		rospy.Subscriber("/tf_pose/kinect_image", Image, self.image_callback)
		rospy.Subscriber("/pose_estimator/pose_3d", Persons, self.tfpose_callback)
		rospy.Subscriber("/spr/activate", Activate, self.activate_callback)

		self.activate_pub = rospy.Publisher("/spr/activate", Activate, queue_size=10)
		self.id = activate_id
		self.bridge = CvBridge()
		self.poses = []
		self.color_image = None
		self.activate_flag = False

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

	def activate_callback(self, msg):
		# type:(Activate)->None
		if msg.id == self.id:
			self.activate_flag = True
			self.face_count()
			self.activate_pub.publish(Activate(id=self.id + 1))

	def image_callback(self, image):
		# type: (Image)->None
		try:
			self.color_image = self.bridge.imgmsg_to_cv2(image, "bgr8")
		except CvBridgeError:
			print "Error at CVBridge"

	def tfpose_callback(self, msg):
		# type:(Persons)->None
		self.poses = copy.deepcopy(msg.persons)

	def get_face_rects(self):
		# type:()->list
		rects = []
		for person in self.poses:

			min_point = (sys.float_info.max, sys.float_info.max)
			max_point = (0.0, 0.0)
			center = (-1.0, -1.0)
			for body in person.body_part:
				body_image_x = body.x * 640
				body_image_y = body.y * 480
				if np.isnan(body.z):
					body_image_z = 0
				else:
					body_image_z = body.z

				if 14 <= body.part_id < 18:
					if min_point[0] > body_image_x:
						min_point = (body_image_x, body_image_y, body_image_z)
					if max_point[0] < body_image_x:
						max_point = (body_image_x, body_image_y, body_image_z)
				if body.part_id == 0:
					center = (body_image_x, body_image_y, body.z)
			# 鼻が認識していない場合
			if center[1] == -1:
				center = (
					(min_point[0] + max_point[0]) / 2, (min_point[1] + max_point[1]) / 2,
					(min_point[2] + max_point[2]) / 2)
			if center[2] > 3.5:
				continue
			if int(max_point[0] - min_point[0]) == 11:
				rects = []
				return rects
			x = int(min_point[0])
			y = int(center[1] - ((max_point[0] - min_point[0]) / 2))
			w = int(max_point[0] - min_point[0])
			h = int(max_point[0] - min_point[0])
			rects.append([x, y, w, h])

		return rects

	def face_count(self):
		time.sleep(3)
		while True:
			while self.color_image is None:
				print "画像待機"

			# image_gray = cv2.cvtColor(self.color_image, cv2.COLOR_RGB2GRAY)
			# cascade = cv2.CascadeClassifier(face_cascade_path)
			# face_rects = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(2, 2))
			face_rects = self.get_face_rects()
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
				img_cropped = cv2.resize(self.color_image[y:y + h, x:x + w], (96, 96))  ##パラメータ変更要
				filename = pre_path + ("/img_%02d.png" % i)
				cv2.imwrite(filename, img_cropped)
			m_count = mf.main("男女認識")
			f_count = len(face_rects) - m_count
			self.speak('There are {} people.'.format(len(face_rects)))
			self.speak('There are {0} male and {1} female.'.format(m_count, f_count))
			break


if __name__ == "__main__":
	FaceCut(2)
	rospy.spin()
