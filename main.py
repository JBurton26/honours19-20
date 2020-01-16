from pysense import Pysense
from SI7006A20 import SI7006A20
from network import WLAN
import machine, time
import pycom
import ujson
pycom.heartbeat(False)
py = Pysense()
si = SI7006A20(py)

def main():
    getTemp()
    #connectSink()
    py.setup_sleep(300)
    py.go_to_sleep()

def getTemp():
    print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %")


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
