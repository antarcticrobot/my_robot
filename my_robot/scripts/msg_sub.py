#! /usr/bin/env python
#coding=utf-8
import rospy
from std_msgs.msg import String
# from cam_catch import *
 
def doMsg(msg):
    if(str.find(msg.data,"hello world 10")>=0):
        rospy.loginfo("The right msg")
        # work_thread_rgb82bgr()
        
if __name__ == "__main__":
    rospy.init_node("listener_p")
    sub = rospy.Subscriber("chatter",String,doMsg,queue_size=10)
    rospy.spin()