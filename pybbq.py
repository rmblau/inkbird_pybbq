from bluepy import btle

import struct
import logging
import array

address = "F8:30:02:48:75:17"

SETTINGS_RESULT_UUID = 0xfff1
ACCOUNT_AND_VERIFY_UUID = 0xfff2
HISTORY_DATA_UUID = 0xfff3
REALTIME_DATA_UUID = 0xfff4
SETTINGS_DATA_UUID = 0xfff5

CREDENTIALS_MESSAGE = bytes([0x21, 0x07, 0x06, 0x05, 0x04, 0x03, 0x02, 0x01, 0xb8, 0x22, 0x00, 0x00, 0x00, 0x00, 0x00])
REALTIME_DATA_ENABLE_MESSAGE = bytes([0x0B, 0x01, 0x00, 0x00, 0x00, 0x00])
UNITS_F_MESSAGE = bytes([0x02, 0x01, 0x00, 0x00, 0x00, 0x00])
UNITS_C_MESSAGE = bytes([0x02, 0x00, 0x00, 0x00, 0x00, 0x00])
REQ_BATTERY_MESSAGE = bytes([0x08, 0x24, 0x00, 0x00, 0x00, 0x00])

class Delegate(btle.DefaultDelegate):
    def handleNotification(self, cHandle, data):
        if cHandle == 48:
            self.handleTemperature(data)
        if cHandle == 37:
            self.handleBattery(data)

    def handleTemperature(self, data):
        temp = array.array("H")
        temp.frombytes(data)
        #for probe, t in enumerate(temp):
        #    self.probes[probe + 1].temperature = t
        print( temp )
    
    def handleBattery(self, data):
        if data[0] != 36:
            return
        battery, maxBattery = struct.unpack("<HH", data[1:5])
        battery = int(battery/maxBattery*100)
        #for probe, sensor in self.probes.items():
        #    sensor.battery = battery
        #self.battery.value = battery
        print( battery )

# Connect
client = btle.Peripheral( address )
service = client.getServiceByUUID( "FFF0" )
characteristics = service.getCharacteristics( )
client.setDelegate( Delegate( ) ) 
client.writeCharacteristic( characteristics[0].getHandle() + 1, b"\x01\x00", withResponse=True)
client.writeCharacteristic( characteristics[3].getHandle() + 1, b"\x01\x00", withResponse=True)

# Login
characteristics[1].write(CREDENTIALS_MESSAGE, withResponse=True)

# Enable Data
characteristics[4].write(REALTIME_DATA_ENABLE_MESSAGE, withResponse=True)

# Set Farenheit
characteristics[4].write(UNITS_F_MESSAGE, withResponse=True)
characteristics[4].write(UNITS_F_MESSAGE, withResponse=True)
characteristics[4].write(UNITS_F_MESSAGE, withResponse=True)

# Request Battery
characteristics[4].write(REQ_BATTERY_MESSAGE, withResponse=True)

# Request Temperature
while True:
    service.peripheral.readCharacteristic(characteristics[3].handle)
    characteristics[4].write(REQ_BATTERY_MESSAGE, withResponse=True)