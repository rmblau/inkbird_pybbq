from bluepy  import btle

import struct
import array

import globalVariables



class NotificationDelegate( btle.DefaultDelegate ):
    


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
                    globalVariables.address = dev.addr

            # End if
            
        elif isNewData:
    
            pass

        # End if/else

# End ScanDelegate( )

