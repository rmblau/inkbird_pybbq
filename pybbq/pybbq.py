from elevate import elevate

import sys
import signal

from utilities import device




# -----------------------------------------------------------------------------
# Name: signalHandler
# Abstract: When a signal is sent, especially CTRL+C, make sure to shut down 
#           the application gracefully
# -----------------------------------------------------------------------------
def signalHandler( signal, frame ):

    # Shutdown gracefully
    print( '\nExiting...\n' )

    # Exit with exit status 0
    sys.exit( 0 )

# End signalHandler( )



# -----------------------------------------------------------------------------
# Name: readInformation
# Abstract: After connecting and logging in to the iBBQ device, continually 
#           requests information from the iBBQ device
# -----------------------------------------------------------------------------
def readInformation( ):

    # Continually request information from the iBBQ device
    while True:

        device.requestBattery( )
        device.requestTemperatures( )

    # End while

# End readInformation( )



# -----------------------------------------------------------------------------
# Name: startDeviceCommunication
# Abstract: 
# -----------------------------------------------------------------------------
def startDeviceCommunication( ):

    # Auto scan for the iBBQ thermometer
    device.scanForIBBQ( )

    # Connect to the device
    device.connect( )

    # Login to the device
    device.login( )

    # Enable real time data
    device.enableData( )

    # Set which temperature unit we want to receive
    device.setFarenheit( )       # Currently does not get Farenheit temps from 
    #device.setCelsius( )        # device itself
   
# End startDeviceCommunication( )



# -----------------------------------------------------------------------------
# Name: processInitialization
# Abstract: Initialize some stuff for the process
# -----------------------------------------------------------------------------
def processInitialization( ):

    # Register handler for CTRL+C quitting
    signal.signal( signal.SIGINT, signalHandler )
    
    # Elevate to root permission
    elevate( graphical = False )

# End processInitialization( )



# -----------------------------------------------------------------------------
# Name: startReadingCollection
# Abstract: Start the reading collection process
# -----------------------------------------------------------------------------
def startReadingCollection( ):

    # Continually request information from the iBBQ device
    while True:

        device.requestBattery( )
        device.requestTemperatures( )

    # End while

# End startReadingCollection( )



# -----------------------------------------------------------------------------
# Name: main
# Abstract: Registers a signal handler, elevates to a root process (needed for 
#           bluepy/bluez), scans for and finds the iBBQ device, and lastly 
#           proceeds to continually read information from the iBBQ device
# -----------------------------------------------------------------------------
def main( ):

    # Initialize some stuff for the process
    processInitialization( )

    # Start the device communication
    startDeviceCommunication( )

    # Start reading collection
    startReadingCollection( )

# End main( )



# Run the main method
if __name__ == '__main__':

    main( )

# End if