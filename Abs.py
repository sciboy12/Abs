import evdev
from numpy import interp
from Xlib import X, display
from fractions import Fraction
import pyautogui
import subprocess
import sys
#import re

'''Config section'''
touchpadid='/dev/input/event5'
dev = evdev.InputDevice('/dev/input/event5')
#touchpad_ratio = 0.7181972377
'''End of config'''

'''
Project started Mar. 11, 2019
Prequisutes:
Via APT:
Python3-evdev

Via python3 -m pip:
python-xlib
numpy
subprocess(?)

Notes:
Current ratio is 0.7181972377
run 'sudo evtest' in terminal and choose your touchpad to get min and max values

Todo:
Add config file handling(Have yet to start)
Automate getting touchpad min and max values via evdev(Working on it)
Automate determining screen resolution(Have yet to start)
Seperate root.warp_pointer from the Y calculation algorithm(As it doesn't update the cursor position without updates to ABS_Y, which needs to be fixed)
Automate determining whether to use 'almost equal to' or '=' in code on line 87(Have yet to start, placeholder currently implemented)

Done:
Completed Mar. 12, 2019:
Get script working
Add very basic(Manually configured) ratio compensation
Automate allowing X server connection(Current method is a security risk, will fix later[])
Automate determining touchpad aspect ratio

'''
# Allow Xlib to connect to the X server
# Note that this is a security risk(As it is allowing X server connections from the LAN)
#cmd = ['xhost', '+']
#subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

d = display.Display()
s = d.screen()
root = s.root
device = evdev.InputDevice(touchpadid)
#print(evdev.device.InputDevice.capabilities(device))

#cmd = re.search(evdev.device.InputDevice.capabilities(device))


#evdev.device.AbsInfo(value = 1, min = 0, max = 1000, fuzz=0)

display_resolution_x = 1366
display_resolution_y = 768
'''
# Values for HP 15-f272wm
touchpad_x_min = 1276
touchpad_x_max = 6978

touchpad_y_min = 1044
touchpad_y_max = 4884
'''
# values for Lenovo ThinkPad T480
sensitivity = 100 # In percent
touchpad_x_min = 1266
touchpad_x_max = 5676

touchpad_y_min = 1062
touchpad_y_max = 4690

# WIP Senstivity scaler
#touchpad_x_min_scaled = (sensitivity) * touchpad_x_min / 100
#touchpad_x_max_scaled = (sensitivity) * touchpad_x_max /50

touchpad_x_min_scaled = sensitivity * (touchpad_x_min / 100)
touchpad_x_max_scaled = touchpad_x_max - touchpad_x_min_scaled


touchpad_y_min_scaled = 1 - (sensitivity * touchpad_y_min) / 100
touchpad_y_max_scaled = 1 - (sensitivity * touchpad_y_max) / 100 *6

# Ratio calculation algorithm
touchpad_x_total = touchpad_x_min - touchpad_x_max
touchpad_y_total = touchpad_y_min - touchpad_y_max
print('Touchpad Total Resolution =',str(touchpad_x_total) + 'x' + str(touchpad_y_total))
print('Touchpad X Resolution =',str(touchpad_x_min) + ',' + str(touchpad_x_max))
print('Touchpad Y Resolution =',str(touchpad_y_min) + ',' + str(touchpad_y_max))
print('Touchpad X Resolution(Scaled) =',str(touchpad_x_min_scaled) + ',' + str(touchpad_x_max_scaled))
print('Touchpad Y Resolution(Scaled) =',str(touchpad_y_min_scaled) + ',' + str(touchpad_y_max_scaled))
ratio_dec = touchpad_y_total / touchpad_x_total
print('Touchpad Ratio =', str(Fraction(ratio_dec).limit_denominator(15)))
#print(touchpad_y_min_scaled)
#print(touchpad_y_max_scaled)
#ratio_dec = touchpad_y_total / float(touchpad_x_total)
#print('Touchpad Ratio:')
#ratio_dec = Fraction()
#ratio = Fraction(int(0.7181972377)).limit_denominator()
#
#print(int(ratio))

#value = evdev.events.InputEvent.value
read_loop = device.read_loop
bytype = evdev.ecodes.bytype
#code = evdev.events.InputEvent.code
EV_ABS = evdev.events.EV_ABS
warp_pointer = root.warp_pointer
#event_code =
print('Press Ctrl-C to quit.')
self = touchpadid

try:
    for event in read_loop():
        
        #Check for ABS_X events
        if event.type == EV_ABS and bytype[event.type][event.code] == 'ABS_X':
            
            #default [1276,5696],[0,1366]

            # Map the Touchpad X limits to the screen resolution
            interp_x = int(interp(event.value,[touchpad_x_min,touchpad_x_max],[0,display_resolution_x]))

            #interp_x = int(interp(event.value,[633,11352],[0,1366]))
            #interp_x = int(interp(event.value,[touchpad_x_min * (ratio_dec *2),touchpad_x_max * ratio_dec],[0,1366]))
            #print(interp_x)
            #print(touchpad_x_max_scaled)

        #Check for ABS_Y events
        if event.type == EV_ABS and bytype[event.type][event.code] == 'ABS_Y':

            #default [1044,4884],[0,768]            
            # Map the Touchpad Y limits to the screen resolution
            interp_y = int(interp(event.value,[touchpad_y_min,touchpad_y_max],[0,display_resolution_y]))
            
            # Set the cursor position
            warp_pointer(interp_x,interp_y)
            # Sync the changes
            d.sync()

            # WIP Repalcement for Xlib
            #pyautogui.moveTo(interp_x, interp_y)

            # Report current cursor posistion
            #sys.stdout.write('\r' + "Current coordinates:" + str(interp_x)+ str(interp_y))
            
            #sys.stdout.flush()
            
#        # Maps the Touchpad Y limits to the screen resolution
#        if event.type == evdev.events.EV_ABS and evdev.ecodes.bytype[event.type][event.code] == 'ABS_Y':
#            #default [1044,4884],[0,768]
#            interp_y = int(interp(event.value,[touchpad_y_min,touchpad_y_max],[0,display_resolution_y]))
#            root.warp_pointer(interp_x,interp_y)
#            d.sync()


except KeyboardInterrupt:
    # Closes security hole
    #cmd = ['xhost', '-']
    
    #subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #dev.ungrab
    print('\nExiting...')
    exit()
