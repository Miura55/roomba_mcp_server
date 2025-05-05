import logging
import paho.mqtt.client as mqtt

# ロギングの設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MQTTクライアントの設定
class MQTTClient:
    def __init__(self, broker_host: str = "localhost", broker_port: int = 1883):
        self.client = mqtt.Client()
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.connected = False
        
        # コールバック設定
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        
    def connect(self):
        try:
            self.client.connect(self.broker_host, self.broker_port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            logger.info(f"MQTT接続エラー: {e}")
            return False
    
    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()
        
    def publish(self, topic: str, message: str):
        if not self.connected:
            self.connect()
        
        result = self.client.publish(topic, message)
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            logger.error(f"MQTT公開エラー: {mqtt.error_string(result.rc)}")
            raise Exception(f"MQTT公開エラー: {mqtt.error_string(result.rc)}")
        
        return result
    
    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            logger.info("MQTTブローカーに接続しました")
        else:
            logger.info(f"MQTT接続に失敗しました。リターンコード: {rc}")
            
    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.info(f"MQTTブローカーから切断されました。理由: {rc}")
