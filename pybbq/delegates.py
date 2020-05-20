from bluepy  import btle

import struct
import array

import globalVariables


# -----------------------------------------------------------------------------
# Name: NotificationDelegate
# Abstract: This is the delegate that handles notifications sent by BLE devices
# -----------------------------------------------------------------------------
class NotificationDelegate( btle.DefaultDelegate ):
    


    # -----------------------------------------------------------------------------
    # Name: handleNotification
    # Abstract: When a new notification is sent, decide whether it is a temperature 
    #           reading or battery reading, and call the correct handler
    # -----------------------------------------------------------------------------
    def handleNotification( self, cHandle, data ):
    
        # Is the handle 48?
        if cHandle == 48:

            # Yes, are these temperature readings, send it to the proper handler
            self.handleTemperature( data )

        # End if
        
        # Is the handle 37?
        if cHandle == 37:

            # Yes, its a battery reading, send it to the proper handler
            self.handleBattery( data )

        # End if

    # End handleNotification


    # -----------------------------------------------------------------------------
    # Name: handleTemperature
    # Abstract: When temperature readings is received, handle it here
    # -----------------------------------------------------------------------------
    def handleTemperature( self, data ):
        
        # Begin parsing the temperature information
        temp = array.array( "H" )
        temp.frombytes( data )
        
        #for probe, t in enumerate(temp):
        #    self.probes[probe + 1].temperature = t
        
        # Print out the temperatures that were reported
        print( temp )

    # End handleTemperature
    

    # -----------------------------------------------------------------------------
    # Name: handleBattery
    # Abstract: When a battery reading is received, handle it here
    # -----------------------------------------------------------------------------
    def handleBattery( self, data ):
        
        # Is the first element 36? (Not sure what that means)
        if data[ 0 ] != 36:
            
            # No, do nothing
            return

        # End if
        
        # Begin processing the battery reading/signal
        battery, maxBattery = struct.unpack( "<HH", data[ 1 : 5 ] )
        battery = int( battery / maxBattery * 100 )
        
        #for probe, sensor in self.probes.items():
        #    sensor.battery = battery
        #self.battery.value = battery
        
        # Print out the battery reading (for now)
        print( battery )

    # End handleBattery( )

# End Delegate( )


# -----------------------------------------------------------------------------
# Name: ScanDelegate
# Abstract: This is the delegate used when scanning for BLE devices
# -----------------------------------------------------------------------------
class ScanDelegate( btle.DefaultDelegate ):
    
    

    # -----------------------------------------------------------------------------
    # Name: handleDiscovery
    # Abstract: When a new device is discovered, check to see if this is the iBBQ 
    #           device we are looking for, if so, mark it down as being the address 
    #           desired. Otherwise, continue waiting for new devices to be 
    #           discovered
    # -----------------------------------------------------------------------------
    def handleDiscovery( self, dev, isNewDev, isNewData ):

        # Is this a new device?
        if isNewDev:
    
            # Yes, is this the iBBQ device?
            if dev.getValueText( 9 ) == 'iBBQ':
                    
                    # Yes, tell the user we found it and record the mac address
                    print( '\nFound iBBQ at ', dev.addr, '\n' )
                    globalVariables.address = dev.addr

            # End if
            
        elif isNewData:
    
            # No, pass on this device and wait for the next one
            pass

        # End if/else

# End ScanDelegate( )