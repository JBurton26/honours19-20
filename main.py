from pysense import Pysense
from SI7006A20 import SI7006A20
from mqtt import MQTTClient
from network import WLAN
import machine, time, pycom, json
from machine import Pin
pycom.heartbeat(False)
#########
#Jake Burton
#40278490
#Final Honours Project
#########
# - todo Delete old readings so that the loop within the publisher method doesnt have to iterate through
#           thousands of messages before sending anything.
# - todo Purtify code and sort documentation
#########
#Subscription message handler
#Deals with incoming messages
#########
def sub_cb(topic, msg):
   print(msg)
   publisher(topic, msg)
#########
#Takes a reading and adds it to 'readings.json' found on the SD card
#########
def writeData():
    with open('/nodesd/readings.json', 'r') as file:
        jsons = json.load(file)
    jdict = {'id': len(jsons['readings']),'type':'Temperature', 'value': si.temperature(), 'timestamp': time.localtime()}
    jsons["readings"].append(jdict)
    jdict = {'id': len(jsons['readings']),'type':'Humidity', 'value': si.humidity(), 'timestamp': time.localtime()}
    jsons["readings"].append(jdict)
    with open('/nodesd/readings.json', 'w+') as f:
        f.write(json.dumps(jsons))
    print("Taking Reading")
    return
#########
#Connection to a hardcoded network, sends the initial message that deals with
#the last reading that the sink received
#########
def connectSink(p):
    nets=wlan.scan()
    for net in nets:
        if (net.ssid=="jakepitest"):
            print("Network Found")
            wlan.connect(net.ssid, auth=(net.sec, "jbpi1234"), timeout=5000)
            while not wlan.isconnected(): #Fix so time is taken
                print(".")
                machine.idle() # This linemakes it save soem power
            break
    if(net.ssid=="jakepitest"):
        with open('/nodesd/readings.json', 'r') as file:
            jsons = json.load(file)
        client = jsons["name"]
        print(client)
        mqttcli.set_callback(sub_cb)
        mqttcli.connect()
        mqttcli.subscribe(client)
        jlast = {'name':client}
        mqttcli.publish(topic="lastread", msg=json.dumps(jlast))
        mqttcli.wait_msg()
        waitfor = time.time()+180
        while True:
            if(time.time() >= waitfor):
                machine.idle()
                break
        wlan.disconnect()
#########
#Publisher method
#Takes the arguments fromthe subscription message handler and uses them to determine
#which messages to send to the sink
#########
def publisher(topic, msg):
    with open('/nodesd/readings.json', 'r') as file:
        jsons = json.load(file)
    msgstr = msg.decode('utf-8')
    print(msgstr)
    msgjson = json.loads(msgstr)
    print(msgjson['reading_id'])
    for reading in jsons['readings']:
        if reading['id'] < msgjson['reading_id']:
            continue
        newRead = reading
        newRead['name'] = jsons['name']
        mqttcli.publish(topic="test",msg=json.dumps(newRead))
        #time.sleep(0.05)
    mqttcli.disconnect()
    if(wlan.isconnected()):
        wlan.disconnect()
#########
#Main Method, calls reading method then idles to save some power
#########
def main():
    global waketime
    writeData()
    while True:
        machine.idle()
        if(time.time() >= waketime):
            waketime = time.time()+600
            break
#########
#Loops the main method which calls the other methods
#Initialises all of the necessary variables for the normal function of the node
#########
if __name__ == "__main__":
    wlan = WLAN(mode=WLAN.STA)
    py = Pysense()
    si = SI7006A20(py)
    waketime = time.time()+300
    pinterrupt = Pin('P14', mode=Pin.IN, pull=Pin.PULL_UP)
    pinterrupt.callback(Pin.IRQ_RISING,connectSink)
    with open('/nodesd/readings.json', 'r') as file:
        jsons = json.load(file)
    client = jsons['name']
    mqttcli = MQTTClient(client,"192.168.10.1",user="jakepi",password="jbpi1234", port=1883)
    mqttcli.set_callback(sub_cb)
    while True:
        main()
