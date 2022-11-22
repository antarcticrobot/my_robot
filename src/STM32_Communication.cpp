/**
 * 接受cmd_vel 话题的数据，将其转化成转速指令
 * 然后下发到底盘的STM32控制器中

 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

#include <ros/ros.h>
#include <ros/spinner.h>
#include <sensor_msgs/CameraInfo.h>
#include <sensor_msgs/Image.h>
#include <std_msgs/String.h>

#include <geometry_msgs/Twist.h>
#include <nav_msgs/Odometry.h>
#include <tf/transform_broadcaster.h>

#include <serial/serial.h>
#include <std_msgs/String.h>

#include <sys/time.h>
#include <boost/asio.hpp> //包含boost库函数
#include <boost/bind.hpp>

#include <fstream>
#include <iostream>
#include <sstream>

using namespace std;
using namespace boost::asio; //定义一个命名空间，用于后面的读写操作

//减速比 2006电机减速比为1:36
//减速比 3508电机减速比为1:19
float RATIO[4] = {36.0, 19.0, 1.0, 1.0};
float WHEEL_D[4] = {0.06, 0.012, 0.0667, 0.1}; //轮子直径  m
float HYPOTENUSE = 0.15;
float SCREW_PITCH = 0.004;
float WHEEL_PI = 3.141693; // pi

serial::Serial ros_ser;
ros::Publisher odom_pub;
ros::Publisher chatter_pub;

bool switches[4][10];
double edges[10][2];

bool fixedPointSwitches[4] = {false, false, false, false};
uint32_t parkStartTime[4];
bool parkActionFlag[4][2];

typedef struct
{
  uint32_t counter;

  int32_t total_angle;  //电机转动的总角度
  int16_t speed_rpm;    //转速
  int16_t real_current; //实际的转矩电流
  uint16_t Temp;        //温度

  int32_t round_cnt;     //电机转动圈数
  uint16_t angle;        // abs angle range:[0,8191] 电机转角绝对值
  uint16_t last_angle;   // abs angle range:[0,8191]
  uint16_t offset_angle; //电机启动时候的零偏角度

  uint16_t microswitches;
} moto_measure_t;

moto_measure_t moto_chassis[4] = {0};

union floatData // union的作用为实现char数组和float之间的转换
{
  int32_t int32_dat;
  unsigned char byte_data[4];
} motor_upload_counter, total_angle, round_cnt;
union IntData // union的作用为实现char数组和int16数据类型之间的转换
{
  int16_t int16_dat;
  unsigned char byte_data[2];
} speed_rpm;

void cmd_vel_callback(const geometry_msgs::Twist::ConstPtr &msg);
void send_speed_to_chassis(float x, float y, float w);
void send_rpm_to_chassis(int w1, int w2, int w3, int w4);
void send_to_moto(int num, int mode, int para, bool flag = true);
void clear_odometry_chassis(void);
bool analy_uart_recive_data(std_msgs::String serial_data);
void calculate_position_for_odometry(void);
void publish_odomtery(float position_x, float position_z, float oriention,
                      float vel_linear_x, float vel_linear_z,
                      float vel_angular_w);
void for_show_2022_1106(int count);
void for_show_vel_and_pos(int count, bool fixedPointSwitches);
void send_cam_flag(bool flag);
void motion_test(int count, bool fixedPointSwitches);

int main(int argc, char **argv)
{
  string sub_cmdvel_topic, pub_odom_topic, dev;
  int buad, time_out, hz;
  ros::init(argc, argv, "mickx4");
  ros::NodeHandle n("~");

  n.param<std::string>("sub_cmdvel_topic", sub_cmdvel_topic, "/cmd_vel");
  n.param<std::string>("pub_odom_topic", pub_odom_topic, "/odom");
  n.param<std::string>("dev", dev, "/dev/mick");
  n.param<int>("buad", buad, 115200);
  n.param<int>("time_out", time_out, 1000);
  n.param<int>("hz", hz, 100);

  ros::Subscriber command_sub = n.subscribe(sub_cmdvel_topic, 10, cmd_vel_callback);
  odom_pub = n.advertise<nav_msgs::Odometry>(pub_odom_topic, 20);
  chatter_pub = n.advertise<std_msgs::String>("/chatter", 1000);

  // 开启串口模块
  try
  {
    ros_ser.setPort(dev);
    ros_ser.setBaudrate(buad);
    serial::Timeout to = serial::Timeout::simpleTimeout(1000);
    to.inter_byte_timeout = 1;
    to.read_timeout_constant = 5;
    to.read_timeout_multiplier = 0;
    ros_ser.setTimeout(to);
    ros_ser.open();
    ros_ser.flushInput(); //清空缓冲区数据
  }
  catch (serial::IOException &e)
  {
    ROS_ERROR_STREAM("Unable to open port ");
    return -1;
  }
  if (ros_ser.isOpen())
  {
    ros_ser.flushInput(); //清空缓冲区数据
    ROS_INFO_STREAM("Serial Port opened");
  }
  else
  {
    return -1;
  }

  ros::Rate loop_rate(hz);

  clear_odometry_chassis();
  bool init_OK = true;
  while (!init_OK)
  {
    clear_odometry_chassis();
    ROS_INFO_STREAM("Clear odometry ..... ");
    if (ros_ser.available())
    {
      std_msgs::String serial_data;
      serial_data.data = ros_ser.read(ros_ser.available());

      string str_tem = serial_data.data;
      string::size_type pos = str_tem.find("CLEAR_OK", 0);
      if (pos != string::npos)
        init_OK = true;
    }
    sleep(1);
  }
  ROS_INFO_STREAM("clear odometry successful(mickx4_bringup.cpp) !");
  int count = 0;
  int temp = 0;

  while (ros::ok())
  {
    if (ros_ser.available())
    {
      ROS_INFO_STREAM("ros_ser.available()");
      std_msgs::String serial_data;
      serial_data.data = ros_ser.read(ros_ser.available());

      analy_uart_recive_data(serial_data);
      calculate_position_for_odometry();
    }

    // switches[1][4] == true后30秒内，且两个动作完成前，
    // 保持fixedPointSwitches[0] = true
    if (switches[1][4] == true)
    {
      fixedPointSwitches[0] = true;
      switches[0][0] = switches[0][1] = false;
      parkStartTime[0] = clock();
    }
    else if ((switches[0][0] == true && switches[0][1] == true)) // ||    // clock() - parkStartTime[0] >= 1000 *1000* 30)
    {
      fixedPointSwitches[0] = false;
    }

    // send_to_moto(2, 1, 10);
    for_show_2022_1106(count);
    // for_show_vel_and_pos(count, fixedPointSwitches[0]);

    temp++;
    if (temp == 200)
    {
      count++;
      temp = 0;
    }
    ros::spinOnce();
    loop_rate.sleep();
  }

  std::cout << " EXIT ..." << std::endl;
  ros::waitForShutdown();
  ros::shutdown();
  return 1;
}
//尝试实现……
void motion_test(int count, int tmp, bool fixedPointSwitches)
{
}
//简化相机信号发送，提取出send_cam_flag(bool flag)
void send_cam_flag(bool flag)
{
  std_msgs::String msg;
  msg.data = flag ? "START" : "END";
  ROS_INFO("%s", msg.data.c_str());
  chatter_pub.publish(msg); //向所有订阅 chatter 话题的节点发送消息。
}

//最基础的展示，只是确认速度和位置模式正常
void for_show_vel_and_pos(int count, bool fixedPointSwitches)
{
  if (fixedPointSwitches == false)
  {
    send_cam_flag(false);
    // send_to_moto(1, 1, 400, count % 2 < 1);
    // send_to_moto(2, 1, 10, count % 2 < 1);
    send_to_moto(0, 1, 2000, count % 2 < 1);
    switches[0][0] = switches[0][1] = false;
  }
  else
  {
    send_cam_flag(true);
    // send_to_moto(1, 0, 0);
    // send_to_moto(2, 1, 20, count % 2 < 1);
    if (switches[0][0] == false)
      send_to_moto(0, 1, 2500, false);
    else if (switches[0][1] == false)
    {
      send_to_moto(0, 1, 2500);
    }
  }
}

//最基础的展示，只是为了2022-1106的SRTP拍摄
void for_show_2022_1106(int count)
{
  int stepLen = 10;
  int stage = count % (stepLen * 5);
  if (stage < stepLen * 2)
  {
    send_to_moto(0, 1, 0);
    send_to_moto(1, 1, 400, stage < stepLen * 1);
    send_to_moto(2, 1, 0);
  }
  else if (stage < stepLen * 4)
  {
    send_to_moto(0, 1, 2500, stage < stepLen * 3);
    send_to_moto(1, 1, 0);
    send_to_moto(2, 1, 0);
  }
  else
  {
    send_to_moto(0, 1, 0);
    send_to_moto(1, 1, 0);
    send_to_moto(2, 1, 10, stage < stepLen * 4.5);
  }
}

void cmd_vel_callback(const geometry_msgs::Twist::ConstPtr &msg)
{
  float speed_x, speed_z, speed_w;
  speed_x = msg->linear.x;
  speed_z = msg->linear.z;
  speed_w = msg->angular.z;

  float vel[4];
  vel[0] = speed_z; //左边 //转化为每个轮子的线速度
  vel[1] = speed_x;
  vel[2] = speed_w;

  for (int i = 0; i < 4; i++)
  {
    vel[i] = vel[i] / (WHEEL_D[i] * WHEEL_PI); //转换为轮子的速度　RPM
    vel[i] = vel[i] * RATIO[i] * 60;           //转每秒转换到RPM
  }

  for (int i = 0; i < 4; i++)
  {
    // if (vel[i] >= 0)
    //   send_to_moto(i, 1, vel[i] * 0.1);
    // else
    //   send_to_moto(i, 1, -vel[i] * 0.1, false);
  }

  ROS_INFO_STREAM("vel[0]: " << vel[0] << " vel[1]: " << vel[1] << " vel[2]: " << vel[2] << " vel[3]: " << vel[3]);
  ROS_INFO_STREAM("speed_x:" << msg->linear.x << " speed_z:" << msg->linear.z << " speed_w:" << msg->angular.z);
}

void send_speed_to_chassis(float x, float y, float w) {}

void send_rpm_to_chassis(int w1, int w2, int w3, int w4) {}

void send_to_moto(int num, int mode, int para, bool flag)
{
  int paras[3];
  paras[mode] = para;

  uint8_t data_tem[50];
  unsigned char i, counter = 0;
  unsigned char cmd;
  unsigned int check = 0;

  cmd = 0x05 + num;
  if (flag == false)
    cmd += 4;
  data_tem[counter++] = 0xAA;
  data_tem[counter++] = 0x55;
  data_tem[counter++] = cmd & 0xFF;
  data_tem[counter++] = 0x0A;

  data_tem[counter++] = (mode) % 256;
  data_tem[counter++] = (mode) / 256; //
  data_tem[counter++] = (paras[0]) & 0xFF;
  data_tem[counter++] = (paras[0] >> 8) & 0xFF; //
  data_tem[counter++] = (paras[0] >> 16) & 0xFF;
  data_tem[counter++] = (paras[0] >> 24) & 0xFF; //
  data_tem[counter++] = (paras[1]) % 256;
  data_tem[counter++] = (paras[1]) / 256; //
  data_tem[counter++] = (paras[2]) % 256;
  data_tem[counter++] = (paras[2]) / 256; //

  for (i = 0; i < counter; i++)
  {
    check += data_tem[i];
  }
  data_tem[counter++] = check; // 0xff;
  data_tem[counter++] = 0xEF;
  data_tem[counter++] = 0xFE;

  ros_ser.write(data_tem, 25);
}

void clear_odometry_chassis(void)
{
  uint8_t data_tem[50];
  unsigned char counter = 0;
  unsigned char cmd = 0xE1;
  unsigned int check = 0;

  data_tem[counter++] = 0xAA;
  data_tem[counter++] = 0x55;
  data_tem[counter++] = cmd;
  data_tem[counter++] = 0x00;

  ros_ser.write(data_tem, 25);
}

void readSwitches(int motoNum, int switchNum, int maskNum, int round_cnt)
{
  if ((moto_chassis[motoNum].microswitches & maskNum) == maskNum)
  {
    edges[motoNum][switchNum] = round_cnt;
    switches[motoNum][switchNum] = true;
  }
}

/**
 * @function 解析串口发送过来的数据帧
 * 成功则返回true　否则返回false
 */
bool analy_uart_recive_data(std_msgs::String serial_data)
{
  unsigned char reviced_tem[500];
  uint16_t len = 0, i = 0, j = 0;
  unsigned char check = 0;
  unsigned char tem_last = 0, tem_curr = 0, rec_flag = 0; //定义接收标志位
  uint16_t header_count = 0, step = 0;                    //计数这个数据序列中有多少个帧头
  len = serial_data.data.size();
  if (len < 1 || len > 500)
  {
    ROS_INFO_STREAM("serial data is too short ,  len: " << serial_data.data.size());
    return false; //数据长度太短　
  }
  ROS_INFO_STREAM("Read: " << serial_data.data.size());

  // 有可能帧头不在第一个数组位置
  for (i = 0; i < len; i++)
  {
    tem_last = tem_curr;
    tem_curr = serial_data.data.at(i);
    if (tem_last == 0xAA && tem_curr == 0xFF &&
        rec_flag == 0) //在接受的数据串中找到帧头　
    {
      rec_flag = 1;
      reviced_tem[j++] = tem_last;
      reviced_tem[j++] = tem_curr;
    }
    else if (rec_flag == 1)
    {
      reviced_tem[j++] = serial_data.data.at(i);
      if (tem_last == 0xEF && tem_curr == 0xFE)
      {
        header_count++;
        rec_flag = 2;
      }
    }
    else
      rec_flag = 0;
  }

  ROS_INFO_STREAM("header_count:" << header_count);
  // 检验接受数据的长度
  step = 0;
  int countFrame = 0;
  for (countFrame = 0; countFrame < header_count; countFrame++)
  {
    len = (reviced_tem[3 + step] + 4 + 3); //第一个帧头的长度
    if (reviced_tem[0 + step] == 0xAA && reviced_tem[1 + step] == 0xFF &&
        reviced_tem[len - 2 + step] == 0xEF && reviced_tem[len - 1 + step] == 0xFE)
    { //检查帧头帧尾是否完整

      ROS_INFO_STREAM("recived a frame");
      check = 0x0;
      for (int k = 0; k < len; k++)
      {
        check += reviced_tem[k + step];
      }
      //检验数据长度和校验码是否正确
      // if (reviced_tem[len - 3 + step] != check && reviced_tem[len -
      // 3 + step] != 0xff) return false;

      if (reviced_tem[2 + step] >= 0xA5 &&
          reviced_tem[2 + step] <= 0xA8)
      {
        j = reviced_tem[2 + step] - 0xA5;
        i = 4 + step;
        {
          motor_upload_counter.int32_dat = 0;
          total_angle.int32_dat = 0;
          round_cnt.int32_dat = 0;
          speed_rpm.int16_dat = 0;

          motor_upload_counter.byte_data[0] = reviced_tem[i++];
          motor_upload_counter.byte_data[1] = reviced_tem[i++];
          motor_upload_counter.byte_data[2] = reviced_tem[i++];
          motor_upload_counter.byte_data[3] = reviced_tem[i++];
          total_angle.byte_data[0] = reviced_tem[i++];
          total_angle.byte_data[1] = reviced_tem[i++];
          total_angle.byte_data[2] = reviced_tem[i++];
          total_angle.byte_data[3] = reviced_tem[i++];
          round_cnt.byte_data[0] = reviced_tem[i++];
          round_cnt.byte_data[1] = reviced_tem[i++];
          round_cnt.byte_data[2] = reviced_tem[i++];
          round_cnt.byte_data[3] = reviced_tem[i++];
          speed_rpm.byte_data[0] = reviced_tem[i++];
          speed_rpm.byte_data[1] = reviced_tem[i++];
          moto_chassis[j].angle = reviced_tem[i++] * 256;
          moto_chassis[j].angle += reviced_tem[i++];
          moto_chassis[j].Temp = reviced_tem[i++];
          moto_chassis[j].Temp += reviced_tem[i++] * 256;
          moto_chassis[j].microswitches = reviced_tem[i++];
          moto_chassis[j].microswitches += reviced_tem[i++] * 256;

          readSwitches(j, 0, 0x01, round_cnt.int32_dat);
          readSwitches(j, 1, 0x02, round_cnt.int32_dat);
          readSwitches(j, 2, 0x04, round_cnt.int32_dat);
          readSwitches(j, 3, 0x08, round_cnt.int32_dat);
          switches[j][4] = ((moto_chassis[j].microswitches & 0x10) == 0x10);

          moto_chassis[j].counter = motor_upload_counter.int32_dat;
          moto_chassis[j].total_angle = total_angle.int32_dat;
          moto_chassis[j].round_cnt = round_cnt.int32_dat;
          moto_chassis[j].speed_rpm = speed_rpm.int16_dat;
        }

        ROS_INFO_STREAM("recived motor data, number:" << countFrame);
        // 打印四个电机的转速、转角、温度等信息
        // ROS_INFO_STREAM("M " << j << "  counter: "
        //                      << motor_upload_counter.int32_dat
        //                      << "  t_a: " << moto_chassis[j].total_angle
        //                      << "  n: " << moto_chassis[j].round_cnt
        //                      << " rpm: " << moto_chassis[j].speed_rpm
        //                      << "  a: " << moto_chassis[j].angle);
        // ROS_INFO_STREAM("M " << j << "  Temp: " << moto_chassis[j].Temp
        //                      << "  microswitches: "
        //                      << moto_chassis[j].microswitches
        //                      << "  switches[][0]: " << (switches[j][0])
        //                      << "  switches[][1]: "
        //                      << (switches[j][1] == true ? 1 : 0));

        // ROS_INFO_STREAM("M "
        //                 << "  edges[][0]: " << edges[j][0]
        //                 << "  edges[][1]: " << edges[j][1]);
      }
      else
      {
        ROS_WARN_STREAM("unrecognize frame");
      }
    }
    else
    {
      ROS_WARN_STREAM("frame head is wrong");
      for (int j = 0; j < len; j++)
        cerr << hex << (reviced_tem[j + step] & 0xff) << " ";
    }
    step += len;
  }
  return true;
}
/**
 * @function 利用里程计数据实现位置估计
 *
 */
float distances[3];
float distances_last[3];
float position[3];
float position_screw = -1.0, position_w = 0;
float min_interval[3] = {0.001, 0.001, 0.0001};
float max_interval[3] = {1.0, 1.0, 1.0};
void calculate_position_for_odometry(void)
{
  float distances_delta[4];
  float vel[4];

  float position_delta[3];
  float position_w_delta, position_r_delta;
  float linear_x, linear_z, angular_w;

  ROS_INFO_STREAM("calculate_position_for_odometry");
  //轮子转动的圈数乘以　N*pi*D
  for (int i = 0; i < 3; i++)
  {
    distances_last[i] = distances[i];
    distances[i] = (moto_chassis[i].round_cnt + (moto_chassis[i].total_angle % 8192) / 8192.0) /
                   RATIO[i] * WHEEL_PI * WHEEL_D[i];
    distances_delta[i] = distances[i] - distances_last[i]; //每个轮子位移的增量
    if (abs(distances_delta[i]) < min_interval[i] || abs(distances_delta[i]) > max_interval[i])
      distances_delta[i] = 0;
  }

  ROS_INFO_STREAM("distances_delta[0]: " << distances_delta[0]
                                         << " distances_delta[1]: " << distances_delta[1]
                                         << " distances_delta[2]: " << distances_delta[2]);

  position_delta[0] = distances_delta[1];
  position[0] += position_delta[0];

  position_delta[2] = distances_delta[0];
  position[2] += position_delta[2];
  // if (position_screw < 0)
  //   position[2] = 0;
  // else
  // {
  //   position_screw += distances_delta[0] / (WHEEL_PI * WHEEL_D[0]) * (SCREW_PITCH);
  //   position[2] = sqrt(HYPOTENUSE * HYPOTENUSE - position_screw * position_screw) * 2;
  // }

  position_w_delta = (distances_delta[2]) / float(WHEEL_D[2]); // w, 单位为弧度
  position_w += position_w_delta;
  // if (position_w > 2 * WHEEL_PI)
  //   position_w = position_w - 2 * WHEEL_PI;
  // else if (position_w < -2 * WHEEL_PI)
  //   position_w = position_w + 2 * WHEEL_PI;

  for (int i = 0; i < 4; i++)
    vel[i] = (moto_chassis[i].speed_rpm) / RATIO[i] / 60.0 * WHEEL_PI * WHEEL_D[i];
  linear_x = vel[1];
  linear_z = vel[0];
  angular_w = vel[2];

  ROS_INFO_STREAM("px: " << position[0] << " pz: " << position[2] << " pw: " << position_w);
  ROS_INFO_STREAM("vx: " << linear_x << " vz: " << linear_z << " rw: " << angular_w << endl);

  publish_odomtery(position[0], position[2], position_w, linear_x, linear_z, angular_w);
}

/**
 * @function 发布里程计的数据
 *
 */
void publish_odomtery(float position_x, float position_z, float oriention,
                      float vel_linear_x, float vel_linear_z,
                      float vel_angular_w)
{
  static tf::TransformBroadcaster odom_broadcaster; //定义tf对象
  geometry_msgs::TransformStamped odom_trans;       //创建一个tf发布需要使用的TransformStamped类型消息
  geometry_msgs::Quaternion odom_quat;              //四元数变量
  nav_msgs::Odometry odom;                          //定义里程计对象

  //里程计的偏航角需要转换成四元数才能发布
  odom_quat = tf::createQuaternionMsgFromYaw(oriention); //将偏航角转换成四元数

  //载入坐标（tf）变换时间戳
  odom_trans.header.stamp = ros::Time::now();
  //发布坐标变换的父子坐标系
  odom_trans.header.frame_id = "odom";
  odom_trans.child_frame_id = "base_link";
  // tf位置数据：x,y,z,方向
  odom_trans.transform.translation.x = position_x;
  odom_trans.transform.translation.y = 0.0;
  odom_trans.transform.translation.z = position_z;
  odom_trans.transform.rotation = odom_quat;
  //发布tf坐标变化
  odom_broadcaster.sendTransform(odom_trans);

  //载入里程计时间戳
  odom.header.stamp = ros::Time::now();
  //里程计的父子坐标系
  odom.header.frame_id = "odom";
  odom.child_frame_id = "base_link";
  //里程计位置数据：x,y,z,方向
  odom.pose.pose.position.x = position_x;
  odom.pose.pose.position.y = 0.0;
  odom.pose.pose.position.z = position_z;
  odom.pose.pose.orientation = odom_quat;
  //载入线速度和角速度
  odom.twist.twist.linear.x = vel_linear_x;
  odom.twist.twist.linear.z = vel_linear_z;
  odom.twist.twist.angular.z = vel_angular_w;
  //发布里程计
  odom_pub.publish(odom);
}