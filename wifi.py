# ========================================================================================
#  [FILE NAME]: wifi.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file contains logic for establishing a stationary wifi connection.
# ========================================================================================

import network
import utime
from confidential import credentials as creds

def init_wifi() -> None:

    sta_if = network.WLAN(network.STA_IF)
    
    # Make sure wifi is disconnected to start
    if sta_if.isconnected():
        sta_if.disconnect()
    
    print("Info: Connecting to wifi", end="")
    
    sta_if.active(True)
    
    try:
        sta_if.config(pm=sta_if.PM_NONE) # turn off power saving
    except AttributeError:
        pass

    sta_if.connect(creds['wifi_ssid'], creds['wifi_password'])
    
    retries: int = 20
    while not sta_if.isconnected() and retries > 0:
        print(".", end="")
        utime.sleep(0.5)
        retries -= 1
    
    if retries <= 0:
        print("\nError: Failed to connect to WiFi in allotted time, please reset device.")
        while(1):
            continue
            
    print()
    print("Info: Connected to wifi!")
    
    current_config = list(sta_if.ifconfig())
    current_config[3] = '8.8.8.8' 
    sta_if.ifconfig(tuple(current_config))
    
    print("Info: Network config:", sta_if.ifconfig())
