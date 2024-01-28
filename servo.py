"""
Demo script to control a servo motor.

"""

from myservo import myServo
import time

servo = myServo(7, 50)  # Set servo pin

try:
    while True:       
        for i in range(0, 181, 1):
            servo.myServoWriteAngle(i)  # Set servo angle
            time.sleep_ms(15)
        for i in range(180, 0, -1):
            servo.myServoWriteAngle(i)  # Set servo angle
            time.sleep_ms(15)        
except:
    servo.deinit()
