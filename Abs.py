# Сonfig start
# Enable touchpad buttons/gestures.
# Do note that when set to True, both Abs and the OS will be controlling the cursor.
# This results in single-frame jumps in the cursor position for fast movements.
buttons_on = True
# Config end

import Xlib
import evdev
import re
import numpy
from Xlib import display
from evdev import ecodes, InputDevice
from numpy import interp

# Get display resolution
display=display.Display()
scr=display.screen().root
res=scr.get_geometry()

# Set display resolution
width=res.width
height=res.height

# Set cursor position
warp_pointer=scr.warp_pointer
sync=display.sync

# Detect touchpad
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
        if bool(re.search('Touchpad', device.name)) == True:
                touchpad = InputDevice(device.path)
        if bool(re.search('TouchPad', device.name)) == True:
                touchpad = InputDevice(device.path)

# Set touchpad path
device=touchpad

# Detect min and max touchpad values
capabilities=device.capabilities(verbose=True)
abs_info=capabilities.get(('EV_ABS', 3))
abs_x=dict(abs_info[0:1])
abs_y=dict(abs_info[1:2])

abs_x=abs_x.get(('ABS_X', 0))
abs_y=abs_y.get(('ABS_Y', 1))

# Set min and max touchpad values
x_min=abs_x.min
x_max=abs_x.max
y_min=abs_y.min
y_max=abs_y.max

# Ratio calculation algorithm
x_total=x_min - x_max
y_total=y_min - y_max
ratio=y_total / x_total
y_min_scaled=y_min * (ratio * 2)

y_min=y_min_scaled

print('Press Ctrl-C to quit')

x_old=0
y_old=0
x_new=0
y_new=0
try:
        if buttons_on != True:
                device.grab()
        for event in device.read_loop():
                if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_X:
                        x_new=event.value
                if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_Y:
                        y_new=event.value

                if x_old != x_new or y_old != y_new:
                        warp_pointer(int(interp(x_new,[x_min,x_max],[0,width])), int(interp(y_new,[y_min,y_max],[0,height])))
                        sync()

                if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_X:
                        x_old=event.value
                if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_Y:
                        y_old=event.value
except:
        print("\nExiting")
