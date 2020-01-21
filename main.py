from pysense import Pysense
from SI7006A20 import SI7006A20
from network import WLAN
import machine, time
import pycom
import json
#pycom.heartbeat(False)
py = Pysense()
si = SI7006A20(py)


def main():
    while True:
        writeData()
        py.setup_sleep(10)
        py.go_to_sleep()


def writeData():
    jdict = {'temp': si.temperature(), 'time': rtc.now()}
    with open('/node1sd/readings.json', 'r') as file:
        jsons = json.load(file)
    jsons["readings"].append(jdict)
    #print(jsons)
    with open('/node1sd/readings.json', 'w+') as f:
        f.write(json.dumps(jsons))
    time.sleep(10)

    #with open('/node1sd/readings.json', 'w') as f:
        #ujson.dump(jsonData, f)
    #os.listdir()

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

if __name__ == "__main__":
    main()
