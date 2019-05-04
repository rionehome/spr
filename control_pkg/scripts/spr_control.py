#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
import math
from std_msgs.msg import String
import sys



#define initial angular
angular = 0.0


#Calculate current angular
def Angular(messege):
    global angular
    prinentation_z = messege.pose.pose.orientation.z
    angular = math.degrees(2 * math.asin(prinentation_z))


#Rotate 180 degrees
def Act_1():
    pub_A1 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    vel = Twist()
    vel.linear.x = 0.0
    if angular > -179.5 and angular < 179.5:
        vel.angular.z = 1.0
        pub_A1.publish(vel)
    elif angular > -179.8 and angular < 179.8:
        vel.angular.z = 0.3
        pub_A1.publish(vel)
    else:
        vel.angular.z = 0.0
        pub_A1.publish(vel)
        pub_image = Publisher('/contimg', String, 10)
        pub_image.publish('002')
        sys.exit()


#Catch cue from sound, Act_1 execute.
def callback(data):
    if data.data == "001":
        odom = Odometry()
        while not rospy.is_shutdown():
            Act_1()


#Sound source localization
def Act_2(degree):
    pub_A2 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    pub_sound = rospy.Publisher('/timing', String, 10) #End rotate cue 
    vel = Twist()
    vel.linear.x = 0.0
    if degree >= 0.0 and degree < 180.0:
        max_deg = degree + 0.3
        min_deg = degree - 0.3
        if angular < min_deg and angular > max_deg:
            vel.angular.z = 1.0
            pub_A2.publish(vel)
        else:
            vel.angular.z = 0.0
            pub_A2.publish(vel)
            pub_sound.publish('end')
    elif degree > 180.0 and degree <= 360.0:
        degree = degree - 360.0
        max_deg = degree - 0.3
        min_deg = degree + 0.3
        if angular < min_deg and angular > max_deg:
            vel.angular.z = 1.0
            pub_A2.publish(vel)
        else:
            vel.angular.z = 0.0
            pub_A2.publish(vel)
            pub_sound.publish('end')
    else:
        max_deg = degree - 359.5
        min_deg = degree - 0.5
        if angural < min_deg and angular > max_deg:
            vel.angular.z = 1.0
            pub_A2.publish(vel)
        else:
            vel.angular.z = 0.0
            pub_A2.publish(vel)
            pub_sound.publish('end')


#Catch degree from home_respeaker, Act_2 execute.
def callback_2(data):
    degree = data.data
    deg = float(degree) #Change string to float
    Act_2(deg)


if __name__ == '__main__':
    #define node
    rospy.init_node('act1_publisher')
    sub = rospy.Subscriber('/srtcont', String, callback)
    sub_odo = rospy.Subscriber('/odom', Odometry, Angular)
    sub_second = rospy.Subscriber('sound', String, callback_2)
    rospy.spin()
