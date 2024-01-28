"""
A simple servo motor control class.

"""

from machine import Pin, PWM

class myServo(object):
    def __init__(self, pin, hz):
        """
        Initialize the servo motor.

        Args:
        - pin: Pin number to which the servo is connected.
        - hz: Frequency of PWM signal in Hertz.
        """
        self._servo = PWM(Pin(pin), hz) 
    
    def myServoWriteDuty(self, duty):
        """
        Set the duty cycle for the servo motor.

        Args:
        - duty: Duty cycle value (0-1023).
        """
        if duty <= 26:
            duty = 26
        if duty >= 128:
            duty = 128
        self._servo.duty(duty)
        
    def myServoWriteAngle(self, pos):
        """
        Set the angle for the servo motor.

        Args:
        - pos: Angle value (0-180).
        """
        if pos <= 0:
            pos = 0
        if pos >= 180:
            pos = 180
        pos_buffer = (pos / 180) * (128 - 26)
        self._servo.duty(int(pos_buffer) + 26)

    def myServoWriteTime(self, us):
        """
        Set the pulse width for the servo motor.

        Args:
        - us: Pulse width in microseconds (500-2500).
        """
        if us <= 500:
            us = 500
        if us >= 2500:
            us = 2500
        pos_buffer = (1024 * us) / 20000
        self._servo.duty(int(pos_buffer))
        
    def deinit(self):
        """
        Deinitialize the servo motor.
        """
        self._servo.deinit()
