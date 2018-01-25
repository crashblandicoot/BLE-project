# test BLE Scanning software
# jcs 6/8/2014

import blescan
import sys
import time

import bluetooth._bluetooth as bluez
import paho.mqtt.client as mqtt

dev_id = 0
try:
    sock = bluez.hci_open_dev(dev_id)
    print "ble thread started"

except:
    print "error accessing bluetooth device..."
    sys.exit(1)

# OnConnect
def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe("paxton10/location")

# OnMessage
def on_message(client, userdata, msg):
    print "Topic: ", msg.topic+'\nMessage: '+str(msg.payload)

# Get serial number
def getserial():
  # Extract serial from cpuinfo file
  cpuserial = "0000000000000000"
  try:
    f = open('/proc/cpuinfo','r')
    for line in f:
      if line[0:6]=='Serial':
        cpuserial = line[10:26]
    f.close()
  except:
    cpuserial = "ERROR000000000"
 
  return cpuserial

print "Don't sleep"
#time.sleep(60)

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

mqtt_client.username_pw_set("qigzuqfg","i-y3fg6AU1hJ")
mqtt_client.connect("m21.cloudmqtt.com",18117, 60)

pi_id = getserial()

print "pi_id = " + pi_id

mqtt_client.loop_start()

blescan.hci_le_set_scan_parameters(sock)
blescan.hci_enable_le_scan(sock)

while True:
    returnedList = blescan.parse_events(sock, mqtt_client, pi_id, 10)
    print "----------"
    for beacon in returnedList:
        print beacon

mqtt_client.loop_stop()
mqtt_client.disconnect()
