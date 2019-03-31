printf "This script will install the prerequisites for Abs."
printf "Installation will start in 10 seconds."
sleep 10

printf "Starting installation"
sleep 0.5

printf "Updating APT package lists..."
sleep 2
sudo apt-get update

printf "Installing evtest..."
sleep 2
sudo apt-get install evtest

printf "Installing python3-evdev..."
sleep 2
sudo apt-get install python3-evdev

printf "Installing python3-xlib..."
sleep 2
python3 -m pip install python3-xlib

printf "Installing numpy..."
sleep 2
python3 -m pip install numpy

printf "Installing config module..."
sleep 2
python3 -m pip install config
