from adapters.base_adapter import Adapter
import urllib.parse

class OpenCloseSwitchAdapter(Adapter):

    def __init__(self):
        Adapter.__init__(self)

    def handleMqttMessage(self, device, data, action, domoticz_port):
        if action == 'openclose':
            if data == '0':
                command = 'On'
            else:
                command = 'Off'
        elif action == 'startstop':
            if data == 'stop':
                command = 'Stop'
            else:
                return
        else:
            return
		
        params = {
            'param': self.getParamType(),
            'idx': self.determineDeviceId(device),
            'switchcmd': command
        }
        Adapter.callDomoticzApi(self, domoticz_port, urllib.parse.urlencode(params))

    def getBridgeType(self, device):
        return 11

    def getParamType(self):
        return 'switchlight'

    def getTraits(self):
        return [10]
    
    def publishStateFromDomoticzTopic(self, mqtt_client, device, base_topic, message):
        self.publishState(mqtt_client, device, base_topic, message['nvalue'])

    def publishState(self, mqtt_client, device, base_topic, value):
        base_topic = base_topic + '/' + str(self.determineDeviceId(device)) + '/openclose/set'
        mqtt_client.Publish(base_topic, value)

    def determineDeviceId(self, device):
        return device['idx']