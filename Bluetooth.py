"""
This script demonstrates a UART peripheral using Bluetooth Low Energy (BLE).

Usage:
- Connect to the ESP32S3 device using a BLE-compatible application (e.g., LightBlue).
- Send commands "led_on" to turn on an LED connected to Pin 2.
- Send commands "led_off" to turn off the LED.

"""
import bluetooth
import random
import struct
import time
from ble_advertising import advertising_payload
from machine import Pin
from micropython import const

# Define constants
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)

_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

_UART_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX = (
    bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_READ | _FLAG_NOTIFY,
)
_UART_RX = (
    bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E"),
    _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE,
)
_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX, _UART_RX),
)


class BLESimplePeripheral:
    def __init__(self, ble, name="ESP32S3"):
        """
        Initializes the BLE peripheral.

        Args:
        - ble: BLE object.
        - name: Name of the device (default is "ESP32S3").
        """
        self._ble = ble
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle_tx, self._handle_rx),) = self._ble.gatts_register_services((_UART_SERVICE,))
        self._connections = set()   
        self._write_callback = None
        self._payload = advertising_payload(name=name, services=[_UART_UUID])
        self._advertise()

    def _irq(self, event, data):
        """
        Interrupt handler for BLE events.
        """
        # Track connections so we can send notifications.
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            print("New connection", conn_handle)
            print("\nThe BLE connection is successful.")
            self._connections.add(conn_handle)
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            print("Disconnected", conn_handle)
            self._connections.remove(conn_handle)
            # Start advertising again to allow a new connection.
            self._advertise()
        elif event == _IRQ_GATTS_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(value_handle)
            if value_handle == self._handle_rx and self._write_callback:
                self._write_callback(value)

    def send(self, data):
        """
        Sends data to connected devices.

        Args:
        - data: Data to be sent.
        """
        for conn_handle in self._connections:
            self._ble.gatts_notify(conn_handle, self._handle_tx, data)

    def is_connected(self):
        """
        Checks if any device is connected.

        Returns:
        - True if connected, False otherwise.
        """
        return len(self._connections) > 0

    def _advertise(self, interval_us=500000):
        """
        Starts advertising.

        Args:
        - interval_us: Advertising interval in microseconds (default is 500000).
        """
        print("Starting advertising")
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def on_write(self, callback):
        """
        Sets the callback function for write events.

        Args:
        - callback: Callback function to be called when data is written.
        """
        self._write_callback = callback


def demo():
    """
    Main function to demonstrate the UART peripheral.
    """
    ble = bluetooth.BLE()
    p = BLESimplePeripheral(ble)
    
    led=Pin(2,Pin.OUT)
    
    def on_rx(rx_data):
        """
        Callback function for handling received data.
        """
        print("Received: ", rx_data)
        if rx_data == b'led_on':
            led.value(1)
        elif rx_data == b'led_off':
            led.value(0)
        else:
            pass

    p.on_write(on_rx)
    
    print("Please use LightBlue to connect to ESP32S3.")


if __name__ == "__main__":
    demo()
