from bluepy import btle

import os
import sys

from variables import global_vars
from variables import constants
from variables import delegates


# -----------------------------------------------------------------------------
# Name: toggleBluetoothInterface
# Abstract: This is so we can reset the interface (bring down then back up
#           again) as sometimes the BLE stack gets weird and doesn't respond
#           as expected
# -----------------------------------------------------------------------------
def toggleBluetoothInterface():

    # Bring down the interface
    os.system('sudo hciconfig hci0 down')

    # Bring up the interface again
    os.system('sudo hciconfig hci0 up')

# End toggleBluetoothInterface( )


# -----------------------------------------------------------------------------
# Name: scanForIBBQ
# Abstract: Scans for a device named "iBBQ". Tries 3 times, each time with the
#           scan length getting longer. Starts at 2.5 seconds, then tries again
#           for 5 seconds, then tries for 10 seconds. If it is not found,
#           then we exit
# -----------------------------------------------------------------------------
def scanForIBBQ():

    retryCount = 0
    timeout = 2.5

    # As long as we have not found the device and we haven't reached our retry limit
    while global_vars.address == None and retryCount < 3:

        # Toggle the bluetooth interface if it is up, or bring it up if it is down
        toggleBluetoothInterface()

        # Update the user on our progress
        print('Scanning for devices for ', timeout, ' seconds...')

        # Scan for the iBBQ device name and store it's mac address
        global_vars.scanner = btle.Scanner().withDelegate(delegates.ScanDelegate())
        global_vars.scanner.scan(timeout)

        # Did we find the iBBQ device?
        if global_vars.address == None:

            # No, Increment retry count
            retryCount += 1

            # Double the timeout time. Will go 2.5, 5, 10 seconds.
            timeout *= 2

        else:

            # Yes, We have found the device. No need to keep trying
            deviceFound = True

        # End if/else

    # End while

    # Did we find the device?
    if global_vars.address == None and retryCount == 3:

        # No, exit and tell the user we could not find the device
        sys.exit('\nUnable to find the device. Is it on and in range?\n')

    # End if

# End scanForIBBQ


# -----------------------------------------------------------------------------
# Name: connect
# Abstract: Connects to the iBBQ device
# -----------------------------------------------------------------------------
def connect():
    # TODO fix this crap
    # Connect to the iBBQ device
    global_vars.client = btle.Peripheral(global_vars.address)
    global_vars.service = global_vars.client.getServiceByUUID(
        constants.SERVICE_UUID)
    global_vars.characteristics = global_vars.service.getCharacteristics()
    global_vars.client.setDelegate(delegates.NotificationDelegate())

    # Set some parameters for the device
    global_vars.client.writeCharacteristic(
        global_vars.characteristics[0].getHandle() + 1, b"\x01\x00", withResponse=True)
    global_vars.client.writeCharacteristic(
        global_vars.characteristics[3].getHandle() + 1, b"\x01\x00", withResponse=True)

# End connect( )


# -----------------------------------------------------------------------------
# Name: login
# Abstract: Logs in to the iBBQ device
# -----------------------------------------------------------------------------
def login():

    # Login
    global_vars.characteristics[1].write(
        constants.CREDENTIALS_MESSAGE, withResponse=True)

# End login( )


# -----------------------------------------------------------------------------
# Name: enableData
# Abstract: Enables the iBBQ device to send us realtime data
# -----------------------------------------------------------------------------
def enableData():

    # Enable realtime data
    global_vars.characteristics[4].write(
        constants.REALTIME_DATA_ENABLE_MESSAGE, withResponse=True)

# End enableData( )


# -----------------------------------------------------------------------------
# Name: setFarenheit
# Abstract: Sets the iBBQ device to report in Farenheit
# -----------------------------------------------------------------------------
def setFarenheit():

    # Set farenheit
    global_vars.characteristics[4].write(
        constants.UNITS_F_MESSAGE, withResponse=True)

# End setFarenheit( )


# -----------------------------------------------------------------------------
# Name: setCelsius
# Abstract: Sets the iBBQ device to report in Celsius
# -----------------------------------------------------------------------------
def setCelsius():

    # Set celsius
    global_vars.characteristics[4].write(
        constants.UNITS_C_MESSAGE, withResponse=True)

# End setCelsius( )


# -----------------------------------------------------------------------------
# Name: requestBattery
# Abstract: Requests the battery status from the iBBQ device
# -----------------------------------------------------------------------------
def requestBattery():

    # Request battery
    global_vars.characteristics[4].write(
        constants.REQ_BATTERY_MESSAGE, withResponse=True)

# End requestBattery( )


# -----------------------------------------------------------------------------
# Name: requestTemperatures
# Abstract: Requests the temperature readings from the iBBQ device
# -----------------------------------------------------------------------------
def requestTemperatures():

    # Request temperatures
    global_vars.service.peripheral.readCharacteristic(
        global_vars.characteristics[3].handle)

# End requestTemperatures( )
