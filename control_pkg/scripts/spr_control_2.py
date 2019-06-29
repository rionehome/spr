#!/usr/bin/env python
import rospy
import math
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import String
import getting_array as ga
import time
#define initial angular
angular = 0.0
orient_z = 0.0


#Calculate current angular
def Angular(messege):
    global angular
    orient_z = messege.pose.pose.orientation.z
    angular = math.degrees(2 * math.asin(orient_z))


#Rotate 180 degrees
def Act_1():
    
    
    vel = Twist()
    vel.linear.x = 0.0
    if angular > -175.5 and angular < 170.0:
        vel.angular.z = 1.0
        pub_A1.publish(vel)
    elif angular >= 170.0 and angular < 179.5:
        vel.angular.z = 0.1
        pub_A1.publish(vel)
    else:
        vel.angular.z = 0.0
        pub_A1.publish(vel)
        
        time.sleep(1)
        pub_image.publish('002')
        sys.exit()


#Catch cue from sound, Act_1 execute.
"""
def callback(data):
    if data.data == "001":
        odom = Odometry()
        while not rospy.is_shutdown():
            Act_1()
"""

#Sound source localization
def Act_2(degree):
    global angular
    print "ok"
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
        if angular < min_deg and angular > max_deg:
            vel.angular.z = 1.0
            pub_A2.publish(vel)
        else:
            vel.angular.z = 0.0
            pub_A2.publish(vel)
            pub_sound.publish('end')


#Catch degree from home_respeaker, Act_2 execute.
def callback(data):
    print data
    deg = float(data.data) #Change string to float
    odom = Odometry()
    while not rospy.is_shutdown():
        Act_1()

if __name__ == '__main__':
    #define node
    rospy.init_node('act1_publisher')
    #pub_A1 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    pub_image = rospy.Publisher('/contimg', String, queue_size=10)
    sub_odo = rospy.Subscriber('/odom', Odometry, Angular)
    #sub = rospy.Subscriber('/srtcont', String, callback)
    pub_A2 = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size=10)
    pub_sound = rospy.Publisher('/timing', String, queue_size=10) #End rotate cue 
    sub_second = rospy.Subscriber('sound', String, callback)
    
    rospy.spin()
    