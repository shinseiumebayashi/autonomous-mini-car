#  Product     : Cokoino Real-Wheel Drive Steering Car Chassis kit
#  Auther      : www.cokoino.com
#  Modification: 2025/05/13

# -*- coding: utf-8 -*-
#!/usr/bin/env python    

import RPi.GPIO as GPIO  # Import RPi.GPIO library
import time              # Import time library
import signal            # Import signal library
import atexit            # Import atexit library

atexit.register(GPIO.cleanup)   # Clean GPIO settings 

servopin = 21   # The servo is connected to the GPO21 pin
GPIO.setmode(GPIO.BCM)  # Set GPIO mode to BCM
GPIO.setup(servopin, GPIO.OUT, initial=False)  
p = GPIO.PWM(servopin,50) # Create PWM object with frequency set to 50Hz
p.start(0)  #Start PWM with an initial duty cycle of 0
time.sleep(2)  #delay 2 seconds

while(True):  
  for i in range(0,181,10):                #Rotate from 0 to 180 degrees
    p.ChangeDutyCycle(2.5 + 10 * i / 180)  #set rotation angle  
    time.sleep(0.02)                       #wait 20ms for the cycle time   
    p.ChangeDutyCycle(0)                   #Initialize 
    time.sleep(0.2)                        #wait 20ms for the cycle time 

  for i in range(181,0,-10):               #Rotate from 180 to 0 degrees
    p.ChangeDutyCycle(2.5 + 10 * i / 180)  #set rotation angle 
    time.sleep(0.02)                       #wait 20ms for the cycle time 
    p.ChangeDutyCycle(0)                   #Initialize 
    time.sleep(0.2)                        #wait 20ms for the cycle time 
