import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
from utils.mqtt_client import MQTTClient
from schemes import MoveCommand

# Roombaコントローラークラス
class RoombaController:
    def __init__(self, mqtt_client: MQTTClient):
        self.mqtt_client = mqtt_client
        self.cmd_topic = "roomba/cmd"
    
    def move(self, command: MoveCommand):
        message = json.dumps({
            "type": "move",
            "data":{
                "velocity": command.velocity,
                "yaw_rate": command.yaw_rate,
                "duration": command.duration
            }
        })
        
        return self.mqtt_client.publish(self.cmd_topic, message)
    
    def home(self):
        message = json.dumps({
            "type": "home"
        })
        
        return self.mqtt_client.publish(self.cmd_topic, message)
