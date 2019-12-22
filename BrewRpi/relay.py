
#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time, os


GPIO.setmode(GPIO.BOARD)

RELAIS_1_GPIO = 11
GPIO.setup(RELAIS_1_GPIO, GPIO.OUT) # GPIO Assign mode
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
time.sleep(10)
GPIO.output(RELAIS_1_GPIO, GPIO.HIGH) # on
time.sleep(10)
GPIO.output(RELAIS_1_GPIO, GPIO.LOW) # out
