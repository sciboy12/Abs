# Abs

I created this program as a Linux alternative for apsun's [AbsoluteTouch](https://github.com/apsun/AbsoluteTouch), as I had recently switched to Linux, and couldn't find any alternatives.

Do note that I am still very new to Python (And Git, for that matter).

Please do not hesitate if you have any sugesstions, questions etc.

Tested on Linux Mint 19.1

## Prerequisites
* A laptop with a Synaptics touchpad (others may work, check if the device reports ABS_X and ABS_Y)

* Python 3.6.7 (other versions are untested, but might work).

* python3-evdev

* python3-xlib

* numpy

## Setup
Optional - run setup.sh as root (note that this script will not work on non Ubuntu/Debian-based distros.)

Or manually install:
```
sudo apt-get update
sudo apt-get install evtest python3-evdev
pip3 install python3-xlib numpy
```

## Note:
If you have previously added your user to the input group, then I strongly recommend you undo this change using:
```
sudo gpasswd -d $USER input
```
I say this because i've since discovered that this is a security risk, allowing all programs read access to all input devices, without root.

## Configuration
I have not yet implemented a config file, so all configuration must be done in the code itself.

See the config section of Abs.py for more info.

## Offcial Discord
https://discord.gg/vKJfPyU
Feel free to hang out, chat, and discuss Abs and other projects.

## Todo

Add config file handling

Add Windows support

## Done:

Get screen resolution automatically

Touchpad aspect ratio compensation

Request root only if needed

Get touchpad limits and path automatically(thanks RotatingSpinner)
