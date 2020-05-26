from elevate import elevate

import sys
import signal

import device_utils



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

# End signal_handler( )



# -----------------------------------------------------------------------------
# Name: readInformation
# Abstract: After connecting and logging in to the iBBQ device, continually 
#           requests information from the iBBQ device
# -----------------------------------------------------------------------------
def readInformation( ):

    device_utils.connect( )

    device_utils.login( )

    device_utils.enableData( )

    device_utils.setFarenheit( )
    #device_utils.setCelsius( )
   
    # Continually request information from the iBBQ device
    while True:

        device_utils.requestBattery( )
        device_utils.requestTemperatures( )

    # End while

# End readInformation( )



# -----------------------------------------------------------------------------
# Name: main
# Abstract: Registers a signal handler, elevates to a root process (needed for 
#           bluepy/bluez), scans for and finds the iBBQ device, and lastly 
#           proceeds to continually read information from the iBBQ device
# -----------------------------------------------------------------------------
def main( ):

    # Register handler for CTRL+C quitting
    signal.signal( signal.SIGINT, signalHandler )
    
    # Elevate to root permission
    elevate( graphical = False )

    # Auto scan for the iBBQ thermometer
    device_utils.scanForIBBQ( )

    # Proceed ( this is a place holder until more is methodized )
    readInformation( )

# End main( )



# Run the main method
if __name__ == '__main__':

    main( )

# End if