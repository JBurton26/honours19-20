# boot.py -- run on boot-up
import os, machine,time
from network import WLAN
#os.mkfs('/flash')
#print("Wake Trigger")
sd = machine.SD()
rtc = machine.RTC()
rtc.init((2020,1,28,14,13,0,0,0))
os.mount(sd,'/node1sd')
print("BOOTING")
