"""
Demo script to read IR commands using an IR receiver.

"""

from irrecvdata import irGetCMD

recvPin = irGetCMD(21)  # Initialize IR receiver on pin 21

try:
    while True:
        irValue = recvPin.ir_read()
        if irValue:
            print(irValue)
except:
    pass
