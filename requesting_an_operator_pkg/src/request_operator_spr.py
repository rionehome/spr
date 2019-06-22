#!/usr/bin/env python
import rospy
import sys
import cv2
import os
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
import male_female_predict as mf
dammy = os.path.abspath('request_operator_pkg.py')
face_cascade_path = dammy.replace("/src/request_operator_spr.py",
								  "/etc/opencv-3.1.1/data/haarcascades/haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(face_cascade_path)
ORG_WINDOW_NAME = "cap"
GAUSSIAN_WINDOW_NAME = "cap_gray"

class Face_cut:
	def __init__(self):
		self.subx=rospy.Subscriber("/camera/rgb/image_raw",Image,self.get_image)
		self.pub3 = rospy.Publisher("messenger", String, queue_size=10, latch=True)
		self.bridge = CvBridge()
		self.image_org = None

	def get_image(self,img):
		 self.image_org = self.bridge.imgmsg_to_cv2(img,"bgr8")
	def listener(self):
		rospy.Subscriber("face_cut", String, self.main)
	def main(self,msg):
		print "get"+msg.data
		if self.image_org is None:
			self.sub = rospy.Subscriber("/camera/rgb/image_raw", Image, self.get_image)
		
		image_gray = cv2.cvtColor(self.image_org, cv2.COLOR_BGR2GRAY)
		cascade = cv2.CascadeClassifier(face_cascade)
		facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.2, minNeighbors=2, minSize=(2, 2))
		print facerect
		cv2.imwrite("/home/matsudayamato/images/img_crowd.jpg", self.image_org)
		dir_path = "/home/matsudayamato/RoboCup2018_SPR/images/predict"
		if os.path.exists(dir_path) == False:
			os.mkdir(dir_path)
		
		for i in range(len(facerect)):
			[x,y,w,h] = facerect[i]
			print facerect[i]
			imgCroped = cv2.resize(self.image_org[y:y + h, x:x + w], (96, 96))##パラメータ変更要
			filename = dir_path + ("/img_%02d.jpg" % i)
			cv2.imwrite(filename, imgCroped)
		self.pub3.publish('03')
		m_count = mf.main()
		f_count = facerect -m_count



# Todo  def recognize_gender()


# Todo  def choice_operetor():
# pub03 = rospy.Publisher('detect_face', String, queue_size=10)
# pub03.publish('03')
# sys.exit()

def callback(data):
	if data.data == '02':
		f = Face_cut()
		f.main()
# recognize_gender()
# choice_operetor()

if __name__ == "__main__":
	rospy.init_node('req_operator_spr')
	sub02 = rospy.Subscriber('face_recognize', String, callback)
	rospy.spin()
