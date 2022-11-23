#! /usr/bin/env python
# coding=utf-8
import rospy
from tf.transformations import *
from std_msgs.msg import String
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry


def doMsg(msg):
    if (str.find(msg.data, "hello world 10") >= 0):
        rospy.loginfo("The right msg")


def pstringlistener():
    rospy.init_node("listener_p")
    rospy.Subscriber("chatter", String, doMsg, queue_size=10)
    rospy.spin()


def get_pos(data):
    (roll, pitch, yaw) = euler_from_quaternion(
        [data.orientation.x, data.orientation.y, data.orientation.z, data.orientation.w])
    rospy.loginfo("current position(x:%f,y:%f,z:%f),theta:%f",
                  data.position.x, data.position.y, data.position.z, yaw)


def poslistener():
    rospy.init_node('poslistener', anonymous=True)
    rospy.Subscriber("odom", Pose, get_pos, queue_size=10)
    rospy.spin()


def get_odom(data):
    rospy.loginfo(data)


def odomlistener():
    rospy.init_node('odomlistener', anonymous=True)
    rospy.Subscriber("odom", Odometry, get_odom, queue_size=10)
    rospy.spin()


if __name__ == "__main__":
    # pstringlistener();
    # poslistener()
    odomlistener()
