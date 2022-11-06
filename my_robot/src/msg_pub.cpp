#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sstream>

/**
 * This tutorial demonstrates simple sending of messages over the ROS system.
 */
int main(int argc, char **argv)
{
  ros::init(argc, argv, "talker");
  ros::NodeHandle n;
  ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
  ros::Rate loop_rate(10);
  int count = 0;
  while (ros::ok())
  {
    std_msgs::String msg;
    if (count%20==0)
      msg.data = "START";
    else
      msg.data = "END";
    ROS_INFO("%s", msg.data.c_str());
    chatter_pub.publish(msg);//向所有订阅 chatter 话题的节点发送消息。

    ros::spinOnce();
    loop_rate.sleep();
    ++count;
  }
  return 0;
}
