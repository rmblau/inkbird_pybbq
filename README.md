# inkbird_pybbq
Use raspberry pi to interface over bluetooth low energy (BLE) with an Inkbird IBT-6XS so we can log cook graphs and get a web interface. 

You will need to install bluez on the raspberry pi. I used the following resource as a guide while installing the latest version (5.9 as of 05/08/2020) https://www.argenox.com/library/bluetooth-low-energy/using-raspberry-pi-ble/

inkbird_pybbq is housed in the pybbq folder. You will need to install the requirements in requirements.txt (pip install -r requirements.txt). inkbird_pybbq utilizes a sqlite database to log information from cooks.

ToDo:
    1.) Implement try/catch and logging functions for all methods
    2.) Create sqlite structure/schema and get it built during the initialization of a new db
    3.) Need to somehow check db integrity on start to make sure nothing is corrupt
    4.) Need a method to gracefully disconnect from database
    5.) Begin building a web interface
    6.) Try to get device to report fahrenheit over BLE instead of celsius*10