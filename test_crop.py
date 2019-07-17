#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PIL
import face_recognition

import cv2
import os
import sys
import rospy
import math
from time import sleep
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class Face_Cut():
	def __init__(self):
		#self.sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)
		self.sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.get_image)
		self.node_end = rospy.Publisher("messenger", String, queue_size=10, latch=True)
		self.bridge = CvBridge()
		self.image_org = None

	def get_image(self, img):
		self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")
		
	def topicDetector(self):
		print("I am waiting for topic(face_cut)")
		rospy.Subscriber("face_cut", String, self.main)

	def main(self, msg):
		print(msg.data)
		while self.image_org is None:
			#self.sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)
			self.sub = rospy.Subscriber("/usb_cam/image_raw", Image, self.get_image)
		
		cv2.imwrite("/home/rione/images/test.jpg",self.image_org)
		
		# 画像のpath指定
		imgname = "test"
		#imgpath = imgname + ".jpg"

		imgpath = "/home/rione/images/test.jpg"

		# Dlib
		dlib_img = face_recognition.load_image_file(imgpath)

		# Dlib CNN
		# faces = face_recognition.face_locations(dlib_img, model="cnn")  # CNNモデルで顔認識
		faces = face_recognition.face_locations(dlib_img)  # 顔認識 1s未満 速さと精度のトレードオフ

		print("検出結果" + str(len(faces)) + "人")

		# cropするためにPILで画像を開く
		img = PIL.Image.open(imgpath)

		# 取得したRect（top, right, bottom, left）から 96x96 にcrop
		for i in range(len(faces)):
			[top, right, bottom, left] = faces[i]
			print (faces[i])
			imgCroped = img.crop((left, top, right, bottom)).resize((96, 96))
			filename = "/home/rione/images/predict/%s_%02d.jpg" % (imgname.split(".")[0], i)
			#filename = "%s_%02d.jpg" % (imgname.split(".")[0], i)
			imgCroped.save(filename)

		self.node_end.publish("cut")
		os.system('rosnode kill /spr_facecut')

if __name__ == '__main__':
	rospy.init_node('spr_facecut')
	fd = Face_Cut()
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		fd.topicDetector()
		rate.sleep()
		rospy.spin()
