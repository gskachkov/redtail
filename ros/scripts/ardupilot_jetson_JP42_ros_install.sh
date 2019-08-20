#!/bin/bash

# Copyright (c) 2017, NVIDIA CORPORATION. All rights reserved.
# Full license terms provided in LICENSE.md file.
# Script includes the necessary modifications to run on Jetpack 4.2.x and Ubuntu 18.04

green=`tput setaf 2`
red=`tput setaf 1`
reset=`tput sgr0`

# Should not run this script as sudo.
if [ "$EUID" = 0 ]; then
    echo "${red}Please run this script as a non-root user.${reset}"
    exit
fi

echo "${green}This script will install several components."
echo "Please read license agreement for each component and continue only if you accept the license terms."
echo "ROS Kinetic : http://www.ros.org/"
echo "MAVROS      : http://github.com/mavlink/mavros"
echo "${red}MAVROS note${green} : NVIDIA's use of the MAVROS project is solely under the terms of the BSD license."
echo "gscam       : http://github.com/ros-drivers/gscam"
echo "image_common: http://wiki.ros.org/image_common"
echo "angles      : http://github.com/ros/angles.git"
echo "${reset}"

while true; do
    read -p "Do you accept the license terms of all of the components which are going to be installed? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

# ROS Melodic install. Taken from http://wiki.ros.org/melodic/Installation/Ubuntu with minor modifications.

echo "${green}Installing ROS Melodic ...${reset}"

# Setup your sources.list
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'

# Set up your keys
sudo apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654

# Update package index
sudo apt-get update

# Install ROS base and MAVROS packages
sudo apt-get install -y ros-melodic-ros-base ros-melodic-desktop ros-melodic-mavros ros-melodic-mavros-extras ros-melodic-joy python-catkin-tools tmux ros-melodic-tf2-geometry-msgs

# For some reason, SSL certificates get messed up on TX1 so Python scripts like rosdep will fail. Rehash the certs.
sudo c_rehash /etc/ssl/certs

# MAVROS requires GeographicLib datasets starting v0.20 .
sudo geographiclib-get-geoids egm96-5

# Initialize rosdep
sudo rosdep init
rosdep update

# Environment setup - optional. Do not run if multiple versions of ROS are present.
source /opt/ros/melodic/setup.bash
echo "source /opt/ros/melodic/setup.bash" >> $HOME/.bashrc
source ~/.bashrc

# Install GStreamer plugins (needed for H.264 encoding etc).
echo "${green}Installing GStreamer plugins...${reset}"
sudo apt-get install -y gstreamer1.0-plugins-bad

# Create catkin workspace directory.
CATKIN_WS=$HOME/ws
if [ ! -d "$CATKIN_WS" ]; then
    echo "${green}Creating catkin workspace in $CATKIN_WS...${reset}"
    mkdir -p $CATKIN_WS/src
    cd $CATKIN_WS
    catkin init
fi

# Install camera wrappers and drivers. 
while true; do
	read -p "Do you want to install the ZED Stereo Camera ROS-wrapper (y/n)? If No is selected, the standard libwebcam tool is installed " yn
    case $yn in
        [Yy]* ) 
        # check if ZED SDK is installed
	if [ -d /usr/local/zed ]; then
	   cd $CATKIN_WS/src
           git clone https://github.com/stereolabs/zed-ros-wrapper.git
           cd ../
           catkin_make
           source ./devel/setup.bash
        else
  	   echo "${red}No ZED SDK installation found!"
        fi
        break;;
        [Nn]* ) 
	# install libwebcam command line tool, and disable autofocus and autoexposure
        sudo apt-get install -y uvcdynctrl
        #  disable autofocus and set focus to infinity
        #uvcdynctrl -s "Focus, Auto" 0
        #uvcdynctrl -s "Focus (absolute)" 0
        #  set auto exposure to 'Manual Mode' and set exposure to default value
        #uvcdynctrl -s "Exposure, Auto" 1
        #uvcdynctrl -s "Exposure (Absolute)" 156
	break;;
        * ) echo "Please answer yes or no.";;
    esac
done

exit

# Installing gscam ROS package and its dependencies.
echo "${green}Starting installation of gscam ROS package...${reset}"
echo "Installing dependencies..."
sudo apt-get install -y libgstreamer1.0-dev gstreamer1.0-tools libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev libyaml-cpp-dev

cd $HOME
# Install gscam dependencies.
sudo apt-get install -y ros-kinetic-camera-info-manager ros-kinetic-camera-calibration-parsers ros-kinetic-image-transport

# Install gscam from sources rather than apt-get install as the latter installs a lot of redundant stuff.
cd $HOME
if [ ! -d "$HOME/gscam" ]; then
    echo "Cloning gscam sources..."
    git clone https://github.com/ros-drivers/gscam.git
    cd gscam
else
    echo "Updating gscam sources..."
    cd gscam
    git pull
fi

if [ ! -L "$CATKIN_WS/src/gscam" ]; then
    # Create symlink to catkin workspace.
    ln -s $HOME/gscam $CATKIN_WS/src/
fi

echo "Building gscam package..."
cd $CATKIN_WS
catkin build -DGSTREAMER_VERSION_1_x=On

# Installing redtail ROS packages and dependencies.
echo "${green}Starting installation of caffe_ros and px4_controller ROS packages...${reset}"
cd $HOME
if [ ! -d "$HOME/redtail" ]; then
    echo "Cloning redtail sources..."
    git clone https://github.com/ArduPilot/redtail
else
    echo "Updating redtail sources..."
    cd redtail
    git checkout master
    git pull
fi

if [ ! -L "$CATKIN_WS/src/caffe_ros" ]; then
    # Create symlinks to catkin workspace.
    ln -s $HOME/redtail/ros/packages/caffe_ros $CATKIN_WS/src/
    ln -s $HOME/redtail/ros/packages/px4_controller $CATKIN_WS/src/
    ln -s $HOME/redtail/ros/packages/redtail_debug $CATKIN_WS/src/
fi

echo "Installing dependencies..."
cd $HOME
sudo apt-get install -y ros-kinetic-angles

cd $CATKIN_WS
echo "Building caffe_ros px4_controller redtail_debug packages..."
catkin build

# Environment setup.
echo "source $CATKIN_WS/devel/setup.bash" >> $HOME/.bashrc
source $CATKIN_WS/devel/setup.bash

echo "export ROS_MASTER_URI=http://localhost:11311" >> $HOME/.bashrc
echo "export ROS_IP=127.0.0.1" >> $HOME/.bashrc
source $HOME/.bashrc

echo "${green}All done.${reset}"
