import rospy
from std_msgs.msg import String

if __name__ == "__main__":
	rospy.init_node("test_talker")
	tpc = str(raw_input("topic:"))
	pub = rospy.Publisher(tpc, String, queue_size=10)

	rospy.sleep(2)
	rospy.loginfo(pub)

	message = str(raw_input("message:"))

	pub.publish(message)
