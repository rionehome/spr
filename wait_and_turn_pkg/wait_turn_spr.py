#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String
from geomety_msgs.msg import Twist


def Turn_180():
    pub_A1 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = 0.0
    if angular > - 179.5 and angular < 179.5:
        vel.angular.z = -1.0
        pub_A1.publish(vel)
    elif angular >= 179.5 and angular < 179.8:
        vel.angular.z = -0.3
        pub_A1.publish(vel)
    else:
        vel.angular.z = 0.0
        pub_A1.publish(vel)
        pub02 = rospy.Publisher('face_recognize', String, queue_size=10)
        pub02.publish('02')
        sys.exit()


def callback(data):
    if data.data == '01':
        odom = Odometry()
        while not rospy.is_shutdown():
            Turn_180()
            print("Turn 180 degree.")


if __name__ == '__main__':
    rospy.init_node('wait_turn_spr')
    sud01 = rospy.Subscliber('Turn_180', String, callback)
