import sys



# -----------------------------------------------------------------------------
# Name: convertCToF
# Abstract: Converts celsius to fahrenheit
# -----------------------------------------------------------------------------
def convertCToF( celsius ):

    fahrenheit = celsius * 9 / 5 + 32 # Formula to convert Celsius to Fahrenheit

    return fahrenheit

# End convertCToF



# -----------------------------------------------------------------------------
# Name: signalHandler
# Abstract: When a signal is sent, especially CTRL+C, make sure to shut down 
#           the application gracefully
# -----------------------------------------------------------------------------
def signalExitApp( ):

    # Shutdown gracefully
    print( '\nExiting...\n' )

    # Exit with exit status 0
    sys.exit( 0 )

# End signalHandler( )