#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from sensor_msgs.msg import Image
from subprocess import Popen

packageHolded = True


def callbackDnn(data):
    global packageHolded
    if len(data.data) > 1 and packageHolded:
        rospy.loginfo(rospy.get_caller_id() + 'I see person first time and droping package')
        packageHolded = False
        # Move path to open holder command to variable. It works with Python3, so we run it from outside ros 
        Popen(["python3", "/home/alex/holder/ServoKit/open_holder.py"], close_fds=True)


def listener():
    rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/object_dnn/network/output', Image, callback)
    rospy.spin()

if __name__ == '__main__':
    listener()
