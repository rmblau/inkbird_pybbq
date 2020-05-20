from bluepy  import btle
from elevate import elevate

import struct
import logging
import array
import os
import sys
import signal

import constants



scanner         = None
address         = None
client          = None
service         = None
characteristics = None



class Delegate( btle.DefaultDelegate ):
    


    def handleNotification( self, cHandle, data ):
    
        if cHandle == 48:

            self.handleTemperature( data )

        # End if
        
        if cHandle == 37:

            self.handleBattery( data )

        # End if

    # End handleNotification



    def handleTemperature( self, data ):
        
        temp = array.array( "H" )
        temp.frombytes( data )
        
        #for probe, t in enumerate(temp):
        #    self.probes[probe + 1].temperature = t
        
        print( temp )

    # End handleTemperature
    


    def handleBattery( self, data ):
        
        if data[ 0 ] != 36:
            
            return

        # End if
        
        battery, maxBattery = struct.unpack( "<HH", data[ 1 : 5 ] )
        battery = int( battery / maxBattery * 100 )
        
        #for probe, sensor in self.probes.items():
        #    sensor.battery = battery
        #self.battery.value = battery
        
        print( battery )

    # End handleBattery( )

# End Delegate( )



class ScanDelegate( btle.DefaultDelegate ):
    
    

    def handleDiscovery( self, dev, isNewDev, isNewData ):

        global address
    
        if isNewDev:
    
            if dev.getValueText( 9 ) == 'iBBQ':
                    
                    print( '\nFound iBBQ at ', dev.addr, '\n' )
                    address = dev.addr

            # End if
            
        elif isNewData:
    
            pass

        # End if/else

# End ScanDelegate( )



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

    global scanner
    global address

    retryCount  = 0
    timeout     = 2.5

    while address == None and retryCount < 3:

        # Toggle the bluetooth interface if it is up, or bring it up if it is down
        toggleBluetoothInterface( )

        print( 'Scanning for devices for ', timeout, ' seconds...' )

        # Scan for the iBBQ device name and store it's mac address
        scanner = btle.Scanner( ).withDelegate( ScanDelegate( ) )
        scanner.scan( timeout )

        if address == None:

            # Increment retry count
            retryCount += 1

            # Double the timeout time. Will go 2.5, 5, 10 seconds.
            timeout *= 2

        else:
            
            # We have found the device
            deviceFound = True

        # End if/else

    # End while

    if address == None and retryCount == 3:

        # Did not find the device
        sys.exit( '\nUnable to find the device. Is it on and in range?\n' )
    
    # End if

# End scanForIBBQ


def connect( ):

    global client
    global service
    global characteristics

    # Connect
    client = btle.Peripheral( address )
    service = client.getServiceByUUID( constants.SERVICE_UUID )
    characteristics = service.getCharacteristics( )
    client.setDelegate( Delegate( ) ) 
    client.writeCharacteristic( characteristics[ 0 ].getHandle( ) + 1, b"\x01\x00", withResponse = True )
    client.writeCharacteristic( characteristics[ 3 ].getHandle( ) + 1, b"\x01\x00", withResponse = True )

# End connect( )



def login( ):

    global client
    global service
    global characteristics

    # Login
    characteristics[ 1 ].write( constants.CREDENTIALS_MESSAGE, withResponse = True )

# End login( )



def enableData( ):

    global client
    global service
    global characteristics

    # Enable Data
    characteristics[ 4 ].write( constants.REALTIME_DATA_ENABLE_MESSAGE, withResponse = True )

# End enableData( )



def setFarenheit( ):

    global client
    global service
    global characteristics

    # Set Farenheit
    characteristics[ 4 ].write( constants.UNITS_F_MESSAGE, withResponse = True )

# End setFarenheit( )



def setCelsius( ):

    global client
    global service
    global characteristics

    # Set Celsius
    characteristics[ 4 ].write( constants.UNITS_C_MESSAGE, withResponse = True )

# End setCelsius( )



def requestBattery( ):

    global client
    global service
    global characteristics

     # Request Battery
    characteristics[ 4 ].write( constants.REQ_BATTERY_MESSAGE, withResponse = True )

# End requestBattery( )



def requestTemperatures( ):

    global client
    global service
    global characteristics

    service.peripheral.readCharacteristic( characteristics[ 3 ].handle )
        
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