# Abs

I created this program as a Linux alternative for apsun's [AbsoluteTouch](https://github.com/apsun/AbsoluteTouch), as I had recently switched to Linux, and couldn't find any alternatives.

Do note that I am still very new to Python (And Git, for that matter).

Please do not hesitate if you have any sugesstions, questions etc.

Tested on Linux Mint 19.1

## Prerequisites
A laptop with a Synaptics touchpad (others may work, check if the device reports ABS_X and ABS_Y)

Python 3.6.7 (other versions are untested, but might work).

python3-evdev

python3-xlib

numpy

## Setup and configuration
Optional - run setup.sh as root (note that this script will not work on non Ubuntu/Debian-based distros.)

Or manually install:
```
sudo apt-get update
sudo apt-get install evtest python3-evdev
pip3 install python3-xlib numpy
```
I have not yet implemented a config file, so all configuration must be done in the code itself:

Run:
```
sudo evtest
```
Then select your touchpad, then press Ctrl-C and scroll up to get the min and max values (look for ABS_X and ABS_Y).

Open Abs.py in a text editor or IDE.

Fill in the min and max values from earlier.

Also change /dev/input/event5 to the path representing your touchpad.

## Running
For running Abs, you have two options:


Add your user to the "input" group:
```
usermod -a -G input $USER
```

Or, alternatively, just run Abs as-is, as it will automatically request root permissions if needed.

## Todo

Add config file handling

Get touchpad min and max values automatically


## Done:

Get screen resolution automatically

Touchpad aspect ratio compensation

Request root only if needed
