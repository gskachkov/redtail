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
joyPub = True
switch_on = True
switch_off = True

# def callback(data):
#    global readyToOpen
#    rospy.loginfo(rospy.get_caller_id() + 'I heard %s', len(data.data))
#    if len(data.data) > 1 and readyToOpen:
#        rospy.loginfo(rospy.get_caller_id() + 'I see person first time')
#        readyToOpen = False
#        Popen(["python3", "/home/alex/holder/ServoKit/open_holder.py"], close_fds=True)
#        rospy.loginfo(rospy.get_caller_id() + 'I am droping package')

def getJoyMessage(on, off):
    msg = Joy()
    msg.axes = [0,0,0,0,0,0,]
    msg.buttons = [
            on,
            off,
            0,
            0,
            1,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
        ]
    return msg

def callbackRCIn(data):
    global joyPub
    global switch_on
    global switch_off
    rospy.loginfo(rospy.get_caller_id() + 'I header all %s', data.channels);
    rospy.loginfo(rospy.get_caller_id() + 'I header ' +  str(switch_on) + '-' + str(switch_off));
    if data.channels[6] == 2003 and switch_on:
        joyMsg = getJoyMessage(1, 0)        
        joyPub.publish(joyMsg)
        switch_on = False
        switch_off = True
    elif data.channels[6] == 1024 and switch_off:
        joyMsg = getJoyMessage(0, 1)
        joyPub.publish(joyMsg)
        switch_off = False
        switch_on = True

def listener():
    global joyPub
    rospy.init_node('rc_listener_node')
    mavros.set_namespace('mavros')
    joyPub = rospy.Publisher('/joy', Joy, queue_size=1)
    rospy.Subscriber(mavros.get_topic('rc/in'), RCIn, callbackRCIn)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
