import rospy
import sys

sys.path.remove('/opt/ros/melodic/lib/python2.7/dist-packages')
from std_msgs.msg import String
import cv2
import os

dammy = os.path.abspath('spr_image.py')
face_cascade_path = dammy.replace("/scripts/spr_image.py",
								  "/etc/opencv-3.3.1/data/haarcascades/haarcascade_upperbody.xml")

face_cascade = cv2.CascadeClassifier(face_cascade_path)

ORG_WINDOW_NAME = "cap"
GAUSSIAN_WINDOW_NAME = "cap_gray"


def callback(data):
	if data.data == "004":
		facecount()


def facecount():
	# pub = rospy.Publisher('srtcont',String,queue_size=10)
	global face_list
	cap = cv2.VideoCapture(0)
	end_flag, c_frame = cap.read()
	height, width, channels = c_frame.shape

	cv2.namedWindow(ORG_WINDOW_NAME)
	cv2.namedWindow(GAUSSIAN_WINDOW_NAME)

	while end_flag == True:

		img = c_frame
		img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		face_list = face_cascade.detectMultiScale(img_gray, minSize=(100, 100))

		for x, y, w, h in face_list:
			cv2.rectangle(img_gray, (x, y), (x + w, y + h), (255, 0, 0), 2)
			face = img_gray[y: y + h, x: x + w]
			face_gray = img_gray[y: y + h, x: x + w]

		cv2.imshow(ORG_WINDOW_NAME, c_frame)
		cv2.imshow(GAUSSIAN_WINDOW_NAME, img_gray)

		k = cv2.waitKey(1)
		if k == 27:
			break

		end_flag, c_frame = cap.read()

	print("number of face{}".format(len(face_list)))
	cap.release()
	cv2.destroyAllWindows()
	cv2.waitKey(0)
	cv2.destroyAllWindows()


def listener():
	rospy.Subscriber("/srtqeus", String, callback)
	rospy.spin()


if __name__ == "__main__":
	facecount()
