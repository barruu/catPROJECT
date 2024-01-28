"""
This script uses an ultrasonic sensor to measure distance and prints the result.

Usage:
- Connect an ultrasonic sensor to pins 13 (trigPin) and 14 (echoPin).
- Ensure that the sensor's trigPin is connected to Pin.OUT and echoPin is connected to Pin.IN.
- Supply appropriate power to the sensor.
- Run the script.

"""

from machine import Pin
import time

# Define trigPin and echoPin
trigPin = Pin(13, Pin.OUT, 0)
echoPin = Pin(14, Pin.IN, 0)

# Speed of sound in cm/microsecond
soundVelocity = 340

def getSonar():
    """
    Function to measure distance using an ultrasonic sensor.
    
    Returns:
    - Distance in centimeters (integer).
    """
    trigPin.value(1)  # Send a pulse
    time.sleep_us(10)  # Wait for 10 microseconds
    trigPin.value(0)  # Stop the pulse

    # Wait for the signal to be received
    while not echoPin.value():
        pass
    pingStart = time.ticks_us()

    # Wait for the signal to stop
    while echoPin.value():
        pass
    pingStop = time.ticks_us()

    # Calculate the time difference and convert to distance
    pingTime = time.ticks_diff(pingStop, pingStart)
    distance = pingTime * soundVelocity // 2 // 10000  # Distance formula

    return int(distance)

# Initial delay
time.sleep_ms(2000)

# Continuous loop to measure and print distance
while True:
    time.sleep_ms(500)  # Wait between measurements
    print('Distance:', getSonar(), 'cm')
