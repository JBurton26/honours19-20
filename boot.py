# boot.py -- run on boot-up
import os, machine
#os.mkfs('/flash')
#print("Wake Trigger")
sd = machine.SD()
os.mount(sd,'/node1sd')
