#!/usr/bin/env python
import rospy
import sys
import cv2
import os
import numpy as np
from std_msgs.msg import String

sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
dammy = os.path.abspath('request_operator_pkg.py')
face_cascade_path = dammy.replace("/scripts/spr_image.py",
								  "/etc/opencv-3.1.1/data/haarcascades/haarcascade_frontalface_default.xml")
face_cascade = cv2.CascadeClassifier(face_cascade_path)
ORG_WINDOW_NAME = "cap"
GAUSSIAN_WINDOW_NAME = "cap_gray"


def face_count():
	cap = cv2.VideoCapture(0)
	end_flag, c_frame = cap.read()
	height, width, channels = c_frame.shape
	cv2.namedWindow(ORG_WINDOW_NAME)
	cv2.namedWindow(GAUSSIAN_WINDOW_NAME)
	while end_flag == True:
		image = c_frame
		image_gray = cv2.cvtColor(image, cv2.COLOR_BRG2GRAY)
		face_list = face_cascade.detectMultiScale(image_gray, minSize=(100, 100))
		for x, y, w, h in face_list:
			cv2.rectangle(image_gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
			face = image_gray[y: y + h, x: x + w]
			face_gray = image_gray[y: y + h, x:x + w]
		cv2.imgshow(ORG_WINDOW_NAME, c_frame)
		cv2.imgshow(GAUSSIAN_WINDOW_NAME, image_gray)
		k = cv2.waitKey(1)
		if k == 27:
			break
		end_frag, c_frame = cap.read()
	print("number of face{}".format(len(face_list)))
	cap.release()
	cv2.destroyAllWindows()
	cv2.waitKey(0)
	cv2.destroyAllWindow()


# Todo  def recognize_gender()


# Todo  def choice_operetor():
# pub03 = rospy.Publisher('detect_face', String, queue_size=10)
# pub03.publish('03')
# sys.exit()

def callback(data):
	if data.data == '02':
		face_count()
		# recognize_gender()
		# choice_operetor()


if __name__ == "__main__":
	rospy.init_node('req_operator_spr')
	sub02 = rospy.Subscriber('face_recognize', String, callback)
	rospy.spin()