# boot.py -- run on boot-up
##########
#Jake Burton
#40278490
#Final Honours Project
#########
# - todo Fix RTC initialization to sync with the connectSink
#########
import os, machine,time
from network import WLAN
sd = machine.SD()
rtc = machine.RTC()
rtc.init((2020,3,14,20,50,0,0,0))
os.mount(sd,'/nodesd')
print("BOOTING")
