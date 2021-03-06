#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image, Joy
from subprocess import Popen
import mavros
from mavros_msgs.msg import RCIn
import os

packageHolded = True
joyPub = True
switch_on = True
switch_off = True


def getJoyMessage(on, off):
    msg = Joy()
    msg.axes = [0, 0, 0, 0, 0, 0]
    msg.buttons = [on, off, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return msg


def callbackRCIn(data):
    global joyPub
    global switch_on
    global switch_off

    if data.channels[9] != 1024 and switch_on:
        joyMsg = getJoyMessage(1, 0)        
        joyPub.publish(joyMsg)
        switch_on = False
        switch_off = True
        rospy.loginfo(rospy.get_caller_id() + 'I header: start dnn ')
    elif data.channels[9] == 1024 and switch_off:
        joyMsg = getJoyMessage(0, 1)
        joyPub.publish(joyMsg)
        switch_off = False
        switch_on = True
        rospy.loginfo(rospy.get_caller_id() + 'I header: stop dnn ')


def callbackDnn(data):
    global packageHolded
    if len(data.data) > 1 and packageHolded:
        rospy.loginfo(rospy.get_caller_id() + 'I see person first time and droping package')
        packageHolded = False
        # Move path to open holder command to variable. It works with Python3, so we run it from outside ros 
        Popen(["python3", "/home/alex/holder/ServoKit/open_holder.py"], close_fds=True)


def listener():
    global joyPub
    rospy.init_node('holder_contoller_node')
    rospy.loginfo(rospy.get_caller_id() + "Start work")
    mavros.set_namespace('mavros')

    joyPub = rospy.Publisher('/joy', Joy, queue_size=1)

    rospy.Subscriber(mavros.get_topic('rc/in'), RCIn, callbackRCIn)
    rospy.Subscriber('/object_dnn/network/output', Image, callbackDnn)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    listener()
