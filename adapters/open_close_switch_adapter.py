from adapters.base_adapter import Adapter
import urllib.parse
import re

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
        if value == 0:        # open
            topic = base_topic + '/' + str(self.determineDeviceIdOrName(device)) + '/openclose/set'
            mqtt_client.Publish(topic, '100')
            topic = base_topic + '/' + str(self.determineDeviceIdOrName(device)) + '/startstop/set'
            mqtt_client.Publish(topic, 'start')   # makes possible to stop 

        if value == 1:        # close
            topic = base_topic + '/' + str(self.determineDeviceIdOrName(device)) + '/openclose/set'
            mqtt_client.Publish(topic, '0')
            topic = base_topic + '/' + str(self.determineDeviceIdOrName(device)) + '/startstop/set'
            mqtt_client.Publish(topic, 'start')   # makes possible to start

        if value == 17:       # stop
            topic = base_topic + '/' + str(self.determineDeviceIdOrName(device)) + '/startstop/set'
            mqtt_client.Publish(topic, 'stop')


    def determineDeviceId(self, device):
        return device['idx']

    def determineDeviceIdOrName(self, device):
        if "gBridge" in device['Description']:
            match = re.search('gBridge:(.*)([\n|\r]?)', device['Description'])
            if match:
                res = match.group(1).strip()
            else:
                res = device['idx']
        else:
            res = device['idx']
        return res
