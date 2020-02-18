from pysense import Pysense
from SI7006A20 import SI7006A20
from network import WLAN
import machine, time, pycom, json
#import pycom
#import json
pycom.heartbeat(False)
py = Pysense()
si = SI7006A20(py)
waketime = time.time()+30

def main():
    global waketime
    #writeData()
    #print("Going to Sleep")
    while True:
        machine.idle()
        if(time.time() >= waketime):
            waketime = time.time()+30
            break


#Takes a reading and adds it to 'readings.json' found on the SD card
def writeData():
    with open('/node1sd/readings.json', 'r') as file:
        jsons = json.load(file)
    jdict = {'id': len(jsons['readings']),'temp': si.temperature(), 'hum': si.humidity(), 'time': time.localtime()}
    jsons["readings"].append(jdict)
    with open('/node1sd/readings.json', 'w+') as f:
        f.write(json.dumps(jsons))
    print(jdict)
    #time.sleep(30)

#Connection for a set network to be changed later
def connectSink():
    wlan = WLAN(mode=WLAN.STA)
    print()
    nets=wlan.scan()
    for net in nets:
        if (net.ssid=="Optify_0C81"):
            print("Network Found")
            wlan.connect(net.ssid, auth=(net.sec, "AUQBNHECTR"), timeout=5000)
            while not wlan.isconnected():
                print(".")
                machine.idle() # This linemakes it save soem power
            #print(net.ssid)
            break

#Loops the main method which calls the other methods
if __name__ == "__main__":
    while True:
        main()
