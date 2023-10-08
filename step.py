#!/usr/bin/env python
 
import time
import RPi.GPIO as GPIO
from bmp280 import BMP280
from datetime import datetime

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

# PWM init
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

pwm_pin = 12
GPIO.setup(pwm_pin, GPIO.OUT)
pwm = GPIO.PWM(pwm_pin, 1000)
pwm.start(0)

# Initialise the BMP280
bus = SMBus(1)
bmp280 = BMP280(i2c_dev=bus)

with open("pomiary.txt", "w") as f:
	pwm.ChangeDutyCycle(100)
	while True:
		temperature = bmp280.get_temperature()
		f.write(f"{temperature}\n")
		print(f"[{datetime.now().time()}] {temperature}")
		time.sleep(1)
