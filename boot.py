# boot.py -- run on boot-up
import os, machine
#os.mkfs('/flash')
#print("Wake Trigger")
sd = machine.SD()
rtc = machine.RTC()
rtc.init((2020,1,21,17,45,0,0,0))
os.mount(sd,'/node1sd')
