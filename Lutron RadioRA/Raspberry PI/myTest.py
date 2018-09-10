import json

zoneStates = 'zmp,1000010000100001XXxx100001X0X011'
zoneStates = zoneStates.upper().lstrip('ZMP')

zones = {"name":"Bedroom1", "zoneType":"dimmer","zone":"1","system":"1"},{"name":"Bedroom2", "zoneType":"dimmer","zone":"2","system":"1"},{"name":"Bedroom3", "zoneType":"dimmer","zone":"3","system":"1"}

class zone:
	def __init__(self, name = "", zonetype = "", zone = 0, system = 1):
		self.name = name
		self.zonetype = zonetype
		self.zone = zone
		self.system = system

zones = [zone('Bedroom1',"dimmer",1,1), zone('Bedroom2',"dimmer",3,1), zone('Bedroom3',"dimmer",11,1)]


newzones = []
for index, item in enumerate(zones):
    newzones.append(item.__dict__)
    if zoneStates[item.zone] == '0':
        newzones[index]["state"] = 'off'
    elif zoneStates[item.zone] == '1':
        newzones[index]["state"] = 'on'
    else:
        newzones[index]["state"] = 'unknown'

print (zoneStates)
print (zones)
print (json.dumps(newzones))
