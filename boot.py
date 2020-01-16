# boot.py -- run on boot-up
from network import WLAN
wlan = WLAN(mode=WLAN.STA)
nets = wlan.scan()
for net in nets:
    if net.ssid == 'jblap':
        print('Network Found!')
        wlan.connect(net.ssid, auth=(net.sec, '1234jblt'), timeout=5000)
        print('WLAN connection succeeded"')
        break
