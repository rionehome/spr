#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import rospy
from std_msgs.msg import String

def talker():
	pub = rospy.Publisher('messenger', String, queue_size=10, latch=True)
	sys.stdout.write('送信する文字列を入力してください：')
	message = raw_input()
	rospy.loginfo('送信メッセージ：'+ message)
	pub.publish(message)


if __name__ == '__main__':
	rospy.init_node('talker', anonymous=True)
	rate = rospy.Rate(1)
	while not rospy.is_shutdown():
		talker()
		rate.sleep()
