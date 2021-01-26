#!/usr/bin/python3    
import pyxhook
import time
from CaptureTime import CaptureTime

#20210123 MH: Create CaptureTime object
capTime = CaptureTime()

#20210123 MH: Campture subject name
user = input("Enter your name: ")
capTime.setUser(user)

#20210123 MH: seting total sessions and reps per session
sessionFreq = input("Set number of session: ")
capTime.setSessionFreq(int(sessionFreq))

entryFreq = input("Set number of reps per session: ")
capTime.setEntryFreq(int(entryFreq))

##20210123 MH: Create dictionary which will be use to storage raw times
capTime.CreateDicTimes()

#Create hookmanager
hookman = pyxhook.HookManager()
#Define our callback to fire when a key is pressed down
hookman.KeyDown = capTime.KeyDownEvent
hookman.KeyUp = capTime.KeyUpEvent
#Hook the keyboard
hookman.HookKeyboard()
#Start our listener
hookman.start()

capTime.CalculateKeystrokesDynamics()

#Create a loop to keep the application running
while capTime.running:
 time.sleep(0.1)

#Close the listener when we are done
hookman.cancel()
