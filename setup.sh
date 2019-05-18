#!/bin/bash

printf "This script will install the prerequisites for Abs.\n"
printf "Installation will start in 10 seconds.\n"
sleep 10

printf "Starting installation\n"
sleep 0.5

printf "Installing python3-pip"
sleep 0.25
apt install python3-pip

printf "Installing python-xlib, evdev and numpy"
pip3 install python-xlib evdev numpy

printf "Done."
