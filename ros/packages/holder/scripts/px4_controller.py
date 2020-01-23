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
    rospy.loginfo(rospy.get_caller_id() + 'I header 6 %s', data.channels[6]);
    rospy.loginfo(rospy.get_caller_id() + 'I header 5 %s', data.channels[5]);
    rospy.loginfo(rospy.get_caller_id() + 'I header 4 %s', data.channels[4]);

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('/mavros', anonymous=True)

    #rospy.Subscriber('/joy', Joy, callback)
    rospy.Subscriber('/mavros/rc/in', RCIn, callbackRCIn)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
