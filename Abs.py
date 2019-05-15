#!/usr/bin/env python3

from numpy import interp
from Xlib import X, display
from evdev import InputDevice, ecodes, events
from time import sleep
#from config import Config
from getpass import getuser
import os
import sys
import grp
#import yaml


# Config - FILL THESE IN
touchpadid ='/dev/input/event5'

touchpad_x_min = 1266
touchpad_x_max = 5676

touchpad_y_min = 1062
touchpad_y_max = 4690

# Tradeoff between CPU usage and lag.
# Valid options are: lowlag, lowcpu.
perfmode = 'lowcpu'

# Enable touchpad buttons/gestures.
# Do note that when set to True, both Abs and the OS will be controlling the cursor.
# This results in single-frame jumps in the cursor position for fast movements.
buttons_on = False
# End of config


# Check if root is needed
# Get list of users associated with the 'input' group
groups = grp.getgrnam('input')

# Get current username
user = getuser()
value = [user] in groups
#euid = os.geteuid()
if value == False and user != 'root':
#if value == False and euid != 0:
    
    # Request root permissions
    args = ['sudo', sys.executable] + sys.argv + [os.environ]
    os.execlpe('sudo', *args)


# Misc stuff to help reduce lag
d = display.Display()
s = d.screen()
root = s.root
device = InputDevice(touchpadid)
read_loop = device.read_loop
read_one = device.read_one
bytype = ecodes.bytype
EV_ABS = events.EV_ABS
warp_pointer = root.warp_pointer
self = touchpadid
sync = d.sync

# WIP Config file handling
#configfile = open('config.cfg', 'w')
#configfile = file('config.cfg')
#config = Config(configfile)
#config.save(configfile)

# Get display resolution
resolution = root.get_geometry()
display_resolution_x = resolution.width
display_resolution_y = resolution.height

# WIP sensitivity scaler
#sensitivity = 100 # In percent
#touchpad_x_min_scaled = sensitivity * (touchpad_x_min / 100)
#touchpad_x_max_scaled = touchpad_x_max - touchpad_x_min_scaled
#touchpad_y_min_scaled = 1 - (sensitivity * touchpad_y_min) / 100
#touchpad_y_max_scaled = 1 - (sensitivity * touchpad_y_max) / 100 *6

# Ratio calculation algorithm
touchpad_x_total = touchpad_x_min - touchpad_x_max
touchpad_y_total = touchpad_y_min - touchpad_y_max
ratio_dec = touchpad_y_total / touchpad_x_total

# Partially working, WIP - Scale the Y axis to compensate for ratio differences
touchpad_y_min_scaled = touchpad_y_min * (ratio_dec * 2) # * (ratio_dec)
touchpad_y_max_scaled = touchpad_y_max # * (ratio_dec)



# Debug stuff
#print('Touchpad X Resolution =',str(touchpad_x_min) + ',' + str(touchpad_x_max))
#print('Touchpad Y Resolution =',str(touchpad_y_min) + ',' + str(touchpad_y_max))
#print('Touchpad X Resolution(Scaled) =',str(touchpad_x_min_scaled) + ',' + str(touchpad_x_max_scaled))
#print('Touchpad Y Resolution(Scaled) =',str(touchpad_y_min_scaled) + ',' + str(touchpad_y_max_scaled))
#eventtype = read_loop.event.type





print('Press Ctrl-C to quit.')
try:
    # grab the touchpad, preventing the OS from moving the cursor
    # This also has the side-effect of disabling the touchpad buttons/gestures
    if buttons_on != True:
        device.grab()
    
    if perfmode == 'lowlag':
        # Placeholder values to prevent a NameError
        interp_x = 0
        interp_y = 0
        
        for event in read_loop():
            
            #Check for ABS_X events
            if event.type == EV_ABS and bytype[event.type][event.code] == 'ABS_X':

                # Map the Touchpad X limits to the screen resolution
                interp_x = int(interp(event.value,[touchpad_x_min,touchpad_x_max],[0,display_resolution_x]))

            #Check for ABS_Y events
            if event.type == EV_ABS and bytype[event.type][event.code] == 'ABS_Y':
                
                # Map the Touchpad Y limits to the screen resolution
                interp_y = int(interp(event.value,[touchpad_y_min_scaled,touchpad_y_max_scaled],[0,display_resolution_y]))
                
            # Set the cursor position
            warp_pointer(interp_x,interp_y)

            # Sync the changes
            sync()


    elif perfmode == 'lowcpu':
        # Placeholder values to prevent a NameError
        y_new=1
        y_old=1
        x_new=1
        x_old=1
        
        for event in device.read_loop():
            if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_X:
                x_new = event.value 
            if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_Y:
                y_new = event.value
           
            if x_old != x_new or y_old != y_new:
                warp_pointer(int(interp(x_new,[touchpad_x_min,touchpad_x_max],[0,display_resolution_x])),\
                int(interp(y_new,[touchpad_y_min_scaled,touchpad_y_max_scaled],[0,display_resolution_y])))
                sync()
           

            if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_X:
                x_old = event.value
            if event.type == ecodes.EV_ABS and event.code == ecodes.ABS_Y:
                y_old = event.value

# Exit when Ctrl-C is pressed
except KeyboardInterrupt:   
    print('\nExiting...')
    exit()

