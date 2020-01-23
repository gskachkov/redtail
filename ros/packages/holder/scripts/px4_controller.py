#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image, Joy
from subprocess import Popen
import mavros
#from geometry_msgs.msg import PoseStamped
from mavros_msgs.msg import RCIn 
#from mavros_msgs.srv import CommandBool, SetMode
#from sensor_msgs.msg import NavSatFix

readyToOpen = True
global joyPub 
# def callback(data):
#    global readyToOpen
#    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', len(data.data))
#    if len(data.data) > 1 and readyToOpen:
#        rospy.loginfo(rospy.get_caller_id() + 'I see person first time')
#        readyToOpen = False
#        Popen(["python3", "/home/alex/holder/ServoKit/open_holder.py"], close_fds=True)
#        rospy.loginfo(rospy.get_caller_id() + 'I am droping package')

def callbackRCIn(data):
    rospy.loginfo(rospy.get_caller_id() + 'I header all %s', data.channels);
    #rospy.loginfo(rospy.get_caller_id() + 'I header 6 %s', data.channels[6]);
    #rospy.loginfo(rospy.get_caller_id() + 'I header 5 %s', data.channels[5]);
    #rospy.loginfo(rospy.get_caller_id() + 'I header 4 %s', data.channels[4]);
    if data.channels[6] = 1514 :
        joyMsg = Joy()
        joyMsg.buttons[0] = 1
        joyPub.publish(joy)

def listener():
    rospy.init_node('rc_listener_node')
    mavros.set_namespace('mavros')
    joyPub = rospy.Publisher('/joy', Joy)
    rospy.Subscriber(mavros.get_topic('rc/in'), RCIn, callbackRCIn)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
