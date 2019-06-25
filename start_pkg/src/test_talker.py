import rospy
from std_msgs.msg import String



if __name__ == "__main__":
    rospy.init_node("/test")
    topic=str(input("topic："))
    pub = rospy.Publisher(topic,String,queue_size=10)
    rospy.sleep(2)
    rospy.loginfo(pub)
    message=str(input("message："))
    pub.publish(message)
