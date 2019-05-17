#!/bin/bash

printf "This script will install the prerequisites for Abs.\n"
printf "Installation will start in 10 seconds.\n"
sleep 10

printf "Starting installation\n"
sleep 0.5

printf "Updating APT package lists...\n"
sleep 2
sudo apt-get update

printf "Installing evtest...\n"
sleep 2
sudo apt-get install evtest

printf "Installing python3-evdev...\n"
sleep 2
sudo apt-get install python3-evdev

printf "Installing python3-xlib...\n"
sleep 2
python3 -m pip install python3-xlib

printf "Installing numpy...\n"
sleep 2
python3 -m pip install numpy
