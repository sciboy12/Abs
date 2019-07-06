#!/bin/bash

if [ `id -g` != 0 ]; then
	echo -e "\e[31mrun with sudo\e[0m"
	exit 1
fi

printf "\e[31mThis script will install the prerequisites for Abs.\n"
printf "\e[31mInstallation will start in 10 seconds.\n"

for ((i=10; i>0; i--)); do
	echo -n " $i"
	sleep 1
done
echo ""

printf "\e[31mUpdating package list\n\e[0m"
sleep 2
apt update

printf "\e[31mStarting installation\n\e[0m"
sleep 0.5

printf "\e[31mInstalling python3-pip\n\e[0m"
sleep 0.25
apt install python3-pip -y

printf "\e[31mInstalling python-xlib, evdev and numpy\n\e[0m"
pip3 install python-xlib evdev numpy

printf "\e[32mDone.\n\e[0m"
