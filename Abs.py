from numpy import interp
from Xlib import X, display
from fractions import Fraction
from screeninfo import get_monitors
import evdev
import subprocess
import sys

# Config - FILL THESE IN
touchpadid='/dev/input/event5'

touchpad_x_min = 1266
touchpad_x_max = 5676

touchpad_y_min = 1062
touchpad_y_max = 4690
# End of config

# Get display resolution
resolution = display.Display().screen().root.get_geometry()
display_resolution_x = resolution.width
display_resolution_y = resolution.height

# WIP sensitivity scaler
#sensitivity = 100 # In percent
#touchpad_x_min_scaled = sensitivity * (touchpad_x_min / 100)
#touchpad_x_max_scaled = touchpad_x_max - touchpad_x_min_scaled
#touchpad_y_min_scaled = 1 - (sensitivity * touchpad_y_min) / 100
#touchpad_y_max_scaled = 1 - (sensitivity * touchpad_y_max) / 100 *6

# WIP Ratio calculation algorithm
#touchpad_x_total = touchpad_x_min - touchpad_x_max
#touchpad_y_total = touchpad_y_min - touchpad_y_max
#ratio_dec = touchpad_y_total / touchpad_x_total

# Misc stuff to help speed up the loop
d = display.Display()
s = d.screen()
root = s.root
device = evdev.InputDevice(touchpadid)
read_loop = device.read_loop
bytype = evdev.ecodes.bytype
EV_ABS = evdev.events.EV_ABS
warp_pointer = root.warp_pointer
self = touchpadid

# Debug stuff
#print('Touchpad X Resolution =',str(touchpad_x_min) + ',' + str(touchpad_x_max))
#print('Touchpad Y Resolution =',str(touchpad_y_min) + ',' + str(touchpad_y_max))
#print('Touchpad X Resolution(Scaled) =',str(touchpad_x_min_scaled) + ',' + str(touchpad_x_max_scaled))
#print('Touchpad Y Resolution(Scaled) =',str(touchpad_y_min_scaled) + ',' + str(touchpad_y_max_scaled))

print('Press Ctrl-C to quit.')
try:
    for event in read_loop():
        
        #Check for ABS_X events
        if event.type == EV_ABS and bytype[event.type][event.code] == 'ABS_X':

            # Map the Touchpad X limits to the screen resolution
            interp_x = int(interp(event.value,[touchpad_x_min,touchpad_x_max],[0,display_resolution_x]))

        #Check for ABS_Y events
        if event.type == EV_ABS and bytype[event.type][event.code] == 'ABS_Y':
            
            # Map the Touchpad Y limits to the screen resolution
            interp_y = int(interp(event.value,[touchpad_y_min,touchpad_y_max],[0,display_resolution_y]))
            
            # Set the cursor position
            warp_pointer(interp_x,interp_y)
            # Sync the changes
            d.sync()
            
# Exit when Ctrl-C is pressed
except KeyboardInterrupt:    
    print('\nExiting...')
    exit()
