#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
使用方法
roslaunchでフリーネクトlaunchを起動する。
kinectの接続を確認する
kinectに分類対象の群衆を映す(imageviewノードなどで映像を確認)
facecut3.pyを実行
images/predict/ディレクトリに分類対象の画像が保存される
次にpredict.pyを実行すると上記のディレクトリに保存された画像を男女分類してくれる
"""
import rospy
import cv2
import sys
import os
import shutil
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge, CvBridgeError

class Face_Cut():
	def __init__(self):
		self.sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)
		self.node_end = rospy.Publisher("messenger", String, queue_size=10, latch=True)
		self.bridge = CvBridge()
		self.image_org = None

	def get_image(self, img):
		self.image_org = self.bridge.imgmsg_to_cv2(img, "bgr8")  # 画像をOpenCVに変換

	def topicDetector(self):
		print("I am waiting for topic(face_cut)")
		rospy.Subscriber("face_cut", String, self.main)
	
	def main(self, msg):
		print(msg)

		while self.image_org is None:
			self.sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)

		#グレースケール変換
		image_gray = cv2.cvtColor(self.image_org, cv2.COLOR_BGR2GRAY)

		#カスケード分類器の特徴量を取得する
		cascade_path = '/home/yoshiwo/opencv-3.1.0/data/haarcascades/haarcascade_frontalcatface.xml'

		cascade = cv2.CascadeClassifier(cascade_path)

		#物体認識（顔認識）の実行
		facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(2, 2))

		print "face rectangle"
		print facerect

		cv2.imwrite("/home/yoshiwo/images/img_crowd.jpg", self.image_org)

		#ディレクトリの作成
		dir_path = "/home/yoshiwo/images/predict"
		#if os.path.exists(dir_path) == False:
		#	os.mkdir(dir_path)

		#img = Image.fromarray(self.image_org)
		for i in range(len(facerect)):
			[x,y,w,h] = facerect[i]
			print facerect[i]
			imgCroped = cv2.resize(self.image_org[y:y + h, x:x + w], (96, 96))
			filename = dir_path + ("/img_%02d.jpg" % i)
			cv2.imwrite(filename, imgCroped)

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

