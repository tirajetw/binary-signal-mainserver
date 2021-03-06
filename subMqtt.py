import paho.mqtt.client as mqttClient
import time

line_url = 'https://notify-api.line.me/api/notify'
token = 'testtest'
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")

def on_message(client, userdata, message):
    print("\nLocation Check-In received: ", message.payload)
    data = message.payload
    # msg = data
    # r = requests.post(line_url, headers=headers , data = {'message':msg})
    # print r.text

Connected = False   #global variable for the state of the connection
 
broker_address= "66.42.54.79"  #Broker address
port = 1883                         #Broker port
user = "iqbot"                    #Connection username
password = "admin"            #Connection password
topic = "test"
client = mqttClient.Client("client-01")               #create new instance
client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop

while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe(topic)
 
try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("exiting")
    client.disconnect()
    client.loop_stop()
