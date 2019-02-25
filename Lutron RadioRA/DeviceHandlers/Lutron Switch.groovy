/** 
 *  Lutron Switch courtesy Stephen Harris (stephen@homemations.com) 
 *   
 *  Copyright 2018 Homemations, Inc. 
 * 
 *  Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except 
 *  in compliance with the License. You may obtain a copy of the License at: 
 * 
 *      http://www.apache.org/licenses/LICENSE-2.0 
 * 
 *  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed 
 *  on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License 
 *  for the specific language governing permissions and limitations under the License.  
 */ 
 
metadata { 
    definition (name: "Lutron RadioRA Switch", author: "Stephen Harris", namespace: "homemations") {  
		capability "Actuator"
		capability "Switch"
		capability "Refresh"
		capability "Sensor"
		capability "Health Check"
		capability "Light"

        command "refresh"
	}

	simulator {
		// TODO: define status and reply messages here
	}

	tiles (scale: 2){
		multiAttributeTile(name:"switch", type: "lighting", width: 6, height: 4, canChangeIcon: true){
			tileAttribute ("device.switch", key: "PRIMARY_CONTROL") {
				attributeState "on", label:'${name}', action:"switch.off", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronSwitchRA-icn.png", backgroundColor:"#00A0DC", nextState:"turningOff"
				attributeState "off", label:'${name}', action:"switch.on", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronSwitchRA-icn.png", backgroundColor:"#ffffff", nextState:"turningOn"
				attributeState "turningOn", label:'${name}', action:"switch.off", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronSwitchRA-icn.png", backgroundColor:"#00A0DC", nextState:"turningOff"
				attributeState "turningOff", label:'${name}', action:"switch.on", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronSwitchRA-icn.png", backgroundColor:"#ffffff", nextState:"turningOn"
			}
		}

		standardTile("refresh", "device.refresh", height: 2, width: 2, inactiveLabel: false, decoration: "flat") {
			state "default", label:"", action:"refresh.refresh", icon:"st.secondary.refresh"
		}

		main(["switch"])
		details(["switch", "refresh"])
	}
}

def updated(){ 
	log.info "Entered Method: updated()"
  	
	configure() 
}

def refresh() {
	log.info "Entered Method: refresh()"
		
    // Get latest state of all zones
    log.debug "Device: " + device
	parent.pollZones()
}


def parse(description) {
    log.debug "Entered Method: parse(${description})"

	def results = []
	def map = description
	if (description instanceof String)  {
		log.debug "Hue Bulb stringToMap - ${map}"
		map = stringToMap(description)
	}

	if (map?.name && map?.value) {
		results << createEvent(name: "${map?.name}", value: "${map?.value}")
	}
	results
}

void on() {
	log.info "Entered Method: on()"
    
    parent.on(this)
}

void off() {
	log.info "Entered Method: off()"
    
	parent.off(this)
}