from bluepy import btle
from decimal import Decimal

import struct
import array

from variables import global_vars
from utilities import general


# -----------------------------------------------------------------------------
# Name: NotificationDelegate
# Abstract: This is the delegate that handles notifications sent by BLE devices
# -----------------------------------------------------------------------------
class NotificationDelegate(btle.DefaultDelegate):

    # -----------------------------------------------------------------------------
    # Name: handleNotification
    # Abstract: When a new notification is sent, decide whether it is a temperature
    #           reading or battery reading, and call the correct handler
    # -----------------------------------------------------------------------------
    def handleNotification(self, cHandle, data):

        # Is the handle 48?
        if cHandle == 48:

            # Yes, are these temperature readings, send it to the proper handler
            self.handleTemperature(data)

        # End if

        # Is the handle 37?
        if cHandle == 37:

            # Yes, its a battery reading, send it to the proper handler
            self.handleBattery(data)

        # End if

    # End handleNotification

    # -----------------------------------------------------------------------------
    # Name: handleTemperature
    # Abstract: When temperature readings is received, handle it here
    # -----------------------------------------------------------------------------

    def handleTemperature(self, data):

        # Load up 2 arrays
        ctemps = array.array("H")

        # Fill the array with the temperatures
        ctemps.frombytes(data)

        # Fill each variable the decimal result
        fTempProbe0 = round(Decimal(general.convertCToF(ctemps[0] / 10)), 2)
        fTempProbe1 = round(Decimal(general.convertCToF(ctemps[1] / 10)), 2)
        fTempProbe2 = round(Decimal(general.convertCToF(ctemps[2] / 10)), 2)
        fTempProbe3 = round(Decimal(general.convertCToF(ctemps[3] / 10)), 2)
        fTempProbe4 = round(Decimal(general.convertCToF(ctemps[4] / 10)), 2)
        fTempProbe5 = round(Decimal(general.convertCToF(ctemps[5] / 10)), 2)

        # Add the temperatures to the array
        ftemps = [fTempProbe0, fTempProbe1, fTempProbe2,
                  fTempProbe3, fTempProbe4, fTempProbe5]

        # Output the fahrenheit temps
        print(ftemps)

    # End handleTemperature

    # -----------------------------------------------------------------------------
    # Name: handleBattery
    # Abstract: When a battery reading is received, handle it here
    # -----------------------------------------------------------------------------

    def handleBattery(self, data):

        # Is the first element 36? (Not sure what that means)
        if data[0] != 36:

            # No, do nothing
            return

        # End if

        # Begin processing the battery reading/signal
        battery, maxBattery = struct.unpack("<HH", data[1: 5])
        battery = int(battery / maxBattery * 100)

        # for probe, sensor in self.probes.items():
        #    sensor.battery = battery
        #self.battery.value = battery

        # Print out the battery reading (for now)
        print(battery)

    # End handleBattery( )

# End Delegate( )


# -----------------------------------------------------------------------------
# Name: ScanDelegate
# Abstract: This is the delegate used when scanning for BLE devices
# -----------------------------------------------------------------------------
class ScanDelegate(btle.DefaultDelegate):

    # -----------------------------------------------------------------------------
    # Name: handleDiscovery
    # Abstract: When a new device is discovered, check to see if this is the iBBQ
    #           device we are looking for, if so, mark it down as being the address
    #           desired. Otherwise, continue waiting for new devices to be
    #           discovered
    # -----------------------------------------------------------------------------
    def handleDiscovery(self, dev, isNewDev, isNewData):

        # Is this a new device?
        if isNewDev:

            # Yes, is this the iBBQ device?
            if dev.getValueText(9) == 'iBBQ':

                # Yes, tell the user we found it and record the mac address
                print('\nFound iBBQ at ', dev.addr, '\n')
                global_vars.address = dev.addr

            # End if

        elif isNewData:

            # No, pass on this device and wait for the next one
            pass

        # End if/else

# End ScanDelegate( )
