from bluepy  import btle
from elevate import elevate

import logging
import os
import sys
import signal

import constants
import delegates
import globalVariables



def signalHandler( signal, frame ):

    # Shutdown gracefully
    print( '\nExiting...\n' )

    sys.exit( 0 )

# End signal_handler( )



def toggleBluetoothInterface( ):

    os.system( 'sudo hciconfig hci0 down' )
    os.system( 'sudo hciconfig hci0 up' )

# End toggleBluetoothInterface( )



def scanForIBBQ( ):

    retryCount  = 0
    timeout     = 2.5

    while globalVariables.address == None and retryCount < 3:

        # Toggle the bluetooth interface if it is up, or bring it up if it is down
        toggleBluetoothInterface( )

        print( 'Scanning for devices for ', timeout, ' seconds...' )

        # Scan for the iBBQ device name and store it's mac address
        globalVariables.scanner = btle.Scanner( ).withDelegate( delegates.ScanDelegate( ) )
        globalVariables.scanner.scan( timeout )

        if globalVariables.address == None:

            # Increment retry count
            retryCount += 1

            # Double the timeout time. Will go 2.5, 5, 10 seconds.
            timeout *= 2

        else:
            
            # We have found the device
            deviceFound = True

        # End if/else

    # End while

    if globalVariables.address == None and retryCount == 3:

        # Did not find the device
        sys.exit( '\nUnable to find the device. Is it on and in range?\n' )
    
    # End if

# End scanForIBBQ



def connect( ):

    # Connect
    globalVariables.client          = btle.Peripheral( globalVariables.address )
    globalVariables.service         = globalVariables.client.getServiceByUUID( constants.SERVICE_UUID )
    globalVariables.characteristics = globalVariables.service.getCharacteristics( )

    globalVariables.client.setDelegate( delegates.NotificationDelegate( ) )
    globalVariables.client.writeCharacteristic( globalVariables.characteristics[ 0 ].getHandle( ) + 1, b"\x01\x00", withResponse = True )
    globalVariables.client.writeCharacteristic( globalVariables.characteristics[ 3 ].getHandle( ) + 1, b"\x01\x00", withResponse = True )

# End connect( )



def login( ):

    # Login
    globalVariables.characteristics[ 1 ].write( constants.CREDENTIALS_MESSAGE, withResponse = True )

# End login( )



def enableData( ):

    # Enable Data
    globalVariables.characteristics[ 4 ].write( constants.REALTIME_DATA_ENABLE_MESSAGE, withResponse = True )

# End enableData( )



def setFarenheit( ):

    # Set Farenheit
    globalVariables.characteristics[ 4 ].write( constants.UNITS_F_MESSAGE, withResponse = True )

# End setFarenheit( )



def setCelsius( ):

    # Set Celsius
    globalVariables.characteristics[ 4 ].write( constants.UNITS_C_MESSAGE, withResponse = True )

# End setCelsius( )



def requestBattery( ):

     # Request Battery
    globalVariables.characteristics[ 4 ].write( constants.REQ_BATTERY_MESSAGE, withResponse = True )

# End requestBattery( )



def requestTemperatures( ):

    globalVariables.service.peripheral.readCharacteristic( globalVariables.characteristics[ 3 ].handle )
        
# End requestTemperatures( )



def readInformation( ):

    connect( )

    login( )

    enableData( )

    setFarenheit( )
    #setCelsius( )
   
    while True:

        requestBattery( )
        requestTemperatures( )

    # End while

# End readInformation( )



def main( ):

    # Register handler for CTRL+C quitting
    signal.signal( signal.SIGINT, signalHandler )
    
    # Elevate to root permission
    elevate( graphical = False )

    # Auto scan for the iBBQ thermometer
    scanForIBBQ( )

    # Proceed ( this is a place holder until more is methodized )
    readInformation( )

# End main( )



# Run the main method
if __name__ == '__main__':

    main( )

# End if