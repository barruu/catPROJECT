"""
This script controls a motor using a potentiometer as input.

Usage:
- Connect the motor driver to pins 13 (in1Pin), 14 (in2Pin), and 12 (enablePin).
- Connect a potentiometer to Pin(1) for speed control.
- Run the script.


"""

from machine import ADC, Pin, PWM
import time
import math

# Define pins for motor control
in1Pin = Pin(13, Pin.OUT)
in2Pin = Pin(14, Pin.OUT)
enablePin = Pin(12, Pin.OUT)

# Initialize PWM
pwm = PWM(enablePin, 10000)

# Initialize ADC for potentiometer reading
adc = ADC(Pin(1))
adc.atten(ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)

def driveMotor(dir, spd):
    """
    Function to drive the motor based on direction and speed.

    Args:
    - dir: Direction of rotation (1 for clockwise, 0 for counter-clockwise).
    - spd: Speed of rotation (0 to 4095).
    """
    if dir:
        in1Pin.value(1)
        in2Pin.value(0)
    else:
        in1Pin.value(0)
        in2Pin.value(1)
    pwm.duty(spd)

try:
    while True:
        # Read potentiometer value
        potenVal = adc.read()

        # Determine rotation speed and direction
        rotationSpeed = potenVal - 2048
        if potenVal > 2048:
            rotationDir = 1
        else:
            rotationDir = 0
        rotationSpeed = int(math.fabs((potenVal - 2047) // 2) - 1)

        # Drive the motor
        driveMotor(rotationDir, rotationSpeed)

        # Delay
        time.sleep_ms(10)
except:
    # Cleanup PWM
    pwm.deinit()
