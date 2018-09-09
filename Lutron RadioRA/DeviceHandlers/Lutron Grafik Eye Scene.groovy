/** 
 *  Lutron Grafik Eye Scene courtesy Stephen Harris (stephen@homemations.com) 
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
 * 
 */ 
 
metadata { 
    definition (name: "Lutron Grafik Eye Scene", author: "Stephen Harris", namespace: "homemations") {  
		capability "Switch Level"
		capability "Actuator"
		capability "Switch"
		capability "Refresh"
		capability "Sensor"
		capability "Health Check"
		capability "Light"

        command "refresh"
        command "setRangedLevel", ["number"]
	}

	simulator {
		// TODO: define status and reply messages here
	}

	tiles(scale: 2) {
		multiAttributeTile(name:"switch", type: "lighting", width: 6, height: 4, canChangeIcon: true){
			tileAttribute ("device.switch", key: "PRIMARY_CONTROL") {
				attributeState "on", label:'${name}', action:"switch.off", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronGrafikRA-icn.png", backgroundColor:"#00a0dc", nextState:"turningOff"
				attributeState "off", label:'${name}', action:"switch.on", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronGrafikRA-icn.png", backgroundColor:"#ffffff", nextState:"turningOn"
				attributeState "turningOn", label:'${name}', action:"switch.off", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronGrafikRA-icn.png", backgroundColor:"#00a0dc", nextState:"turningOff"
				attributeState "turningOff", label:'${name}', action:"switch.on", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutronGrafikRA-icn.png", backgroundColor:"#ffffff", nextState:"turningOn"
			}
		}
        
        controlTile("rangeSlider", "device.rangedLevel", "slider", height: 2, width: 4, range: "(0..5)") {
			state "level", action:"setRangedLevel"
		}
        
		standardTile("refresh", "device.switch", width: 2, height: 2, inactiveLabel: false, decoration: "flat") {
			state "default", label:'', action:"refresh.refresh", icon:"st.secondary.refresh"
		}
        
        valueTile("level", "device.level", inactiveLabel: false, decoration: "flat", width: 2, height: 2) {
			state "level", label:'${currentValue}', backgroundColor:"#ffffff"
		}

		main(["switch"])
		details(["switch", "rangeSlider", "refresh"])
	}
}

def updated(){ 
	log.info "Entered Method: updated()"
  	
    configure() 
}

def refresh() {
	log.info "Entered Method: refresh()"
	
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

def on() {
    log.info "Entered Method: on()"
   	
    if (device.currentState("level")?.value == "0") {
    	parent.sendCmd('SGS', device.deviceNetworkId.split(/\./).last(), 5)
        sendEvent(name: "level", value: "5")
        sendEvent(name: "rangedLevel", value: "5")
    } else {
    	parent.sendCmd('SGS', device.deviceNetworkId.split(/\./).last(), device.currentState("level")?.value)
        sendEvent(name: "level", value: "${device.currentState("level")?.value}")
        sendEvent(name: "rangedLevel", value: "${device.currentState("level")?.value}")
	}
    
    sendEvent(name: "switch", value: "on")
}

def off() {
   	log.info "Entered Method: off()"

	parent.sendCmd('SGS', device.deviceNetworkId.split(/\./).last(), 0)
   	sendEvent(name: "switch", value: "off")
    sendEvent(name: "rangedLevel", value: "0")
}

def setRangedLevel(percent) {
   	log.info "Entered Method: setRangedLevel(), Scene: " + percent

    if (verifyPercent(percent)) {
    	parent.sendCmd('SGS', device.deviceNetworkId.split(/\./).last(), percent)
        if (percent > 0) {
			sendEvent(name: "switch", value: "on")
		} else {
			sendEvent(name: "switch", value: "off")
		}
        sendEvent(name: "level", value: "$percent")
        sendEvent(name:"rangedLevel", value: "$percent")
    } 	
}

def verifyPercent(percent) {
	log.info "Entered Method: verifyPercent(), Scene: " + percent
    
    if (percent == null)
        return false
    else if (percent >= 0 && percent <= 5) {
        return true
    } else {
        log.warn "Dimmer Level of $percent is not in the range of 0-5"
        return false
    }
}