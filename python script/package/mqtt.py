import paho.mqtt.client as mqtt
import time
#connecting connected & send destination
class MQTT:
    def __init__(self,clientname):
        self.client=mqtt.Client(clientname)
        self.client.on_message=self.on_message
        self.ESP = 0

    def on_message(self,client,userdata,message):
        print(message.topic)
        print(message.payload.decode("utf-8"))
        if message.payload.decode("utf-8")== "ESP32 Ready to Go":
            self.ESP = 1

        elif message.payload.decode("utf-8") == "Reach Destination":
            self.ESP = 0.5

        elif message.payload.decode("utf-8")== "Task Finished":
            self.ESP = 0.25

        elif message.payload.decode("utf-8")== "Message Received":
            self.ESP = 0

    def start_connection(self):
        self.client.connect("test.mosquitto.org",1883)
        self.client.loop_start()
        self.client.subscribe("Line_Follower_Python")
        self.check_esp_ready()

    def check_esp_ready(self):
        self.client.publish("Line_Follower_ESP32", "Ready?")


    def send_destination(self,DESTINATION):
        self.ESP = 0

        self.client.publish("Line_Follower_ESP32",DESTINATION)

        print(f"publish to {DESTINATION}")

    def status_ESP (self):
        return self.ESP

    def send_signal_back(self):
        self.client.publish("Line_Follower_ESP32", "Balik")