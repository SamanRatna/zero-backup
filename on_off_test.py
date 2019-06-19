import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(3, GPIO.OUT)


for i in range(5):
    GPIO.output(3, GPIO.HIGH)
    print("controller is ON")
    time.sleep(120)
    GPIO.output(3, GPIO.LOW)
    print("controller is OFF")
    time.sleep(120)
