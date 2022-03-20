

import sys
import signal
import os

from utilities import device
from utilities import database
from utilities import general
from variables import constants
from variables import global_vars


# -----------------------------------------------------------------------------
# Name: signalHandler
# Abstract: When a signal is sent, especially CTRL+C, make sure to shut down
#           the application gracefully
# -----------------------------------------------------------------------------
def signalHandler(signal, frame):

    # Call the exit method to clean up and exit cleanly
    return general.signalExitApp()

# End signalHandler( )


# -----------------------------------------------------------------------------
# Name: readInformation
# Abstract: After connecting and logging in to the iBBQ device, continually
#           requests information from the iBBQ device
# -----------------------------------------------------------------------------
def readInformation():

    # Continually request information from the iBBQ device
    while True:

        device.requestBattery()
        device.requestTemperatures()

    # End while

# End readInformation( )


# -----------------------------------------------------------------------------
# Name: startDeviceCommunication
# Abstract:
# -----------------------------------------------------------------------------
def startDeviceCommunication():

    # Auto scan for the iBBQ thermometer
    device.scanForIBBQ()

    # Connect to the device
    device.connect()

    # Login to the device
    device.login()

    # Enable real time data
    device.enableData()

    # Set which temperature unit we want to receive
    device.setFarenheit()       # Currently does not get Farenheit temps from
    # device.setCelsius( )        # device itself

# End startDeviceCommunication( )


# -----------------------------------------------------------------------------
# Name: processInitialization
# Abstract: Initialize some stuff for the process
# -----------------------------------------------------------------------------
def processInitialization():

    # Register handler for CTRL+C quitting
    signal.signal(signal.SIGINT, signalHandler)

    # Elevate to root permission
    # elevate(graphical=False)

# End processInitialization( )


# -----------------------------------------------------------------------------
# Name: startReadingCollection
# Abstract: Start the reading collection process
# -----------------------------------------------------------------------------
def startReadingCollection():

    # Continually request information from the iBBQ device
    while True:

        device.requestBattery()
        device.requestTemperatures()

    # End while

# End startReadingCollection( )


# -----------------------------------------------------------------------------
# Name: initializeGlobalVariables
# Abstract: Gets the current path, adds the db filename, then stores it in
#           global variables
# -----------------------------------------------------------------------------
def initializeGlobalVariables():

    # Populate the global variable with the path
    global_vars.DB_PATH = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), constants.DB_FILENAME)

# End initializeGlobalVariables( )


# -----------------------------------------------------------------------------
# Name: main
# Abstract: Registers a signal handler, elevates to a root process (needed for
#           bluepy/bluez), scans for and finds the iBBQ device, and lastly
#           proceeds to continually read information from the iBBQ device
# -----------------------------------------------------------------------------
def main():

    # Initialize some stuff for the process
    processInitialization()

    # Initialize global variables
    initializeGlobalVariables()

    # Connects to DB if it exists, creates it if it doesn't exist and then
    # connects
    database.createConnectToDatabase()

    # Start the device communication
    startDeviceCommunication()

    # Start reading collection
    startReadingCollection()

# End main( )


# Run the main method
if __name__ == '__main__':

    main()

# End if
