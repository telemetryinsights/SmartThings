/** 
*  Lutron RadioRA Platform Manager via Raspberry PI Gateway by Stephen Harris (stephen@homemations.com) 
*   
*  Copyright 2018 Homemations, Inc 
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
 
// import helper libraries not a part of the SmartThings SDK
import java.text.DecimalFormat
 
definition( 
    name: "Lutron RadioRa (Connect)", 
    namespace: "Homemations", 
    author: "Stephen Harris", 
    description: "This smartapp installs the Lutron RadioRA Platform Manager via Raspberry PI Gateway App that will manage all Lutron zones", 
    category: "Convenience", 
    iconUrl: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutron-icn.png", 
    iconX2Url: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutron-icn@2x.png", 
    iconX3Url: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutron-icn@3x.png", 
    singleInstance: true) 

preferences {	
    page(name: "preferenceLutronManager", title: "Lutron RadioRa")    
    page(name: "preferenceLutronValidation", title: "Lutron RadioRa")    
    page(name: "preferenceLutronConfiguration", title: "Lutron RadioRa")
}

// Functions to return configuration info 
def appVer() { return "1.0.0" }
def getHostAddress() {return platformIP + ":" + platformPort}
def getPlatformUri() {return "/api"}

// Dynamic Preferences to support configuration validation section
def preferenceLutronManager() {
    log.info "Entered Method: preferenceLutronManager()"
    
    atomicState.zones = null
    atomicState.zoneNames = null
    
    def showUninstall = (platformIP != null && platformPort != null)
	return dynamicPage(name: "preferenceLutronManager", title: "Connect to the Lutron RadioRA Platform", nextPage:"preferenceLutronValidation", uninstall: showUninstall) {
		section() {
        	paragraph "Lutron RadioRa (Connect)\n" +
                "Copyright\u00A9 2018 Homemations, Inc.\n" +
            	"Version: ${appVer()}",
                image: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutron-icn.png"
    	}
    
    	section("Platform Credentials") {
        	input("platformIP", "string", title:"IP Address for the Raspberry PI Gateway ", description: "that connects to the Lutron serial port", required: true, displayDuringSetup: true) 
        	input("platformPort", "string", title:"Port # for the Raspberry PI Gateway ", description: "that connects to the Lutron serial port", required: true, displayDuringSetup: true) 		
        }
        
        section("Platform Polling"){
			input(name: "polling", type: "enum", title: "Polling Interval (Minutes)?", description: "The interval to poll the platform for changes", options: [1,5,10,15,30], defaultValue: 5)
		}

		section("Platform Push Notifications") {
        	input "preferencePushAlerts", "bool", required: false, title: "Push notifications when Lutron Zones change?", defaultValue: false
    	}
	}
}

def preferenceLutronValidation() {
    log.info "Entered Method: preferenceLutronValidation()"

	// Config settings for network time out on callback response
	def int timeoutinMilliSeconds = 8000
	def int maxTimeout = now() + timeoutinMilliSeconds
	
	getZones()
	
	// Wait for a connection to the Raspberry PI platform, with timeout set above; need zones list for success
	while (atomicState?.zoneNames == null) {
		if (now().toInteger() > maxTimeout) {
			def pattern = "#,###,###"
			def timeoutFormat = new DecimalFormat(pattern)
			log.warn "Max timeout of " + timeoutFormat.format(timeoutinMilliSeconds) + "mS reached waiting for a response from the Raspberry PI gateway"
			break
		}
	}
	
	if (atomicState?.zoneNames != null) { 
		// Successful connection to Lutron Platform via the Raspberry PI Gateway
		log.warn "Successfully connected to the Lutron Platform via the Raspberry PI Gateway"
		
		return dynamicPage(name: "preferenceLutronConfiguration", title: "Lutron Zones Configuration", install: true, uninstall: true) {
			section("Select Your Lutron Zones") {
				paragraph "Tap below to see the list of Lutorn RadioRA Zones available from your Lutron platform and select the ones you want to connect to SmartThings."
				input(name: "lutronZones", title:"Zones selected", type: "enum", required:true, multiple:true, description: "Tap to choose", metadata:[values: atomicState.zoneNames.sort {it.value}])
			}
		}
	}
	else {
		log.error "Unable to connect to the Lutron platform via the Raspberry PI gateway"
		
		return dynamicPage(name: "preferenceLutronValidation", title: "Lutron Platform Failure", uninstall:false, install: false) {
			section() {
				paragraph "Unable to connect to the Lutron platform."
				paragraph image: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/Lutron/lutron-icn.png",
					title: "Connection Failure",
					required: true,
					"Check to insure that the LAN IP and Port entered is correct and the Raspberry PI gateway is operational.  Press back to verify settings and try again"            
			}
		}
	}
}

def getZones(){
    log.info "Entered Method: getZones()"
	
	try {
		def httpRequest = [
			method: "GET",
			path: getPlatformUri() + "/zones/",
			headers:	[
				HOST: getHostAddress(),
				"Content-Type": "application/json",                        
			]
		]
		
		def hubAction = new physicalgraph.device.HubAction(httpRequest, null, [callback: zonesCallbackHandler])
		return sendHubCommand(hubAction)
	} catch (all) {
		log.error "Cannot connect to the Raspberry PI API services gateway. Message: " + all
	}
    return
}

def zonesCallbackHandler(hubResponse) {
	log.info "Entered Method: ZonesCallbackHandler"
    log.info "Hub Response: " + hubResponse
    
    try {
		def description = hubResponse.description
		def msg = parseLanMessage(description)

		def status = msg.status          // => http status code of the response
		def json = msg.json              // => any JSON included in response body, as a data structure of lists and maps

		log.debug "lanRequest status response: $status" 
		if (status == 200) {
			def zones = [:]
			def zoneNames = [:]

			json.each {zone ->
				def dni = [app.id, zone.zone].join('.')
				zones[dni] = [
					name : zone.name,
					zonetypeid : zone.zonetype_id,
                    zonetype : zone.zonetype,
					system : zone.system,
					level : 0,
					state : zone.state]
				zoneNames[dni] = zone.name
			}

			atomicState.zones = zones
			atomicState.zoneNames = zoneNames
		} else {
			log.error "Not a 200 Response from the Raspberry PI API services gateway"
		}
	} catch (all) {
		log.error "No response from the Raspberry PI API services gateway. Message: " + all
	}
}

def installed() { 
    log.info "Entered Method: installed()"
    log.trace "Installed with settings: ${settings}" 
	
    initialize()
	state.installed = true 
} 
 
def updated() { 
    log.info "Entered Method: updated()"
    log.trace "Updated with settings: ${settings}" 
    
    unschedule()
    unsubscribe() 
    initialize() 
}

def unistalled(){
}
 
def initialize() { 
    log.info "Entered Method: initialize()"
    
    createZoneDevices()
    deleteZoneDevices()

	// Automatically update zone devices status based on the setting for polling
    log.debug "Polling interval: ${polling}"
    switch(polling) {
    	case 1:
        	runEvery1Minutes("pollZones")
            break
    	case 5:
        	runEvery5Minutes("pollZones")
            break
        case 10:
        	runEvery10Minutes("pollZones")
            break
        case 15:
        	runEvery15Minutes("pollZones")
            break
        default:
        	runEvery30Minutes("pollZones")
            break        	
    }
            
    // Send activity feeds to tell that lutron radiora is connected to smartthings
	def notificationMessage = "Lutron RadioRa is now connected to SmartThings"
    sendPush(notificationMessage)

	// atomicState.timeSendPush = null
	// atomicState.reAttempt = 0
}

def createZoneDevices() {
	log.info "Entered Method: createZoneDevices()"
	
    log.debug "Collect: " + lutronZones
    def zones = lutronZones.collect { dni ->
    	def device = getChildDevice(dni)
        def zoneTypeid = atomicState.zones[dni].zonetypeid
        
       	log.debug "Zone details: ${atomicState.zones[dni]}"
        
        if(!device) {
            if (zoneTypeid == 3) {
                device = addChildDevice(app.namespace, "Lutron Grafik Eye Scene", dni, null, ["label":"${atomicState.zones[dni].name}" ?: "Lutron Grafik Eye Scene"])
               	log.debug "Created ${device.displayName} with id $dni as a lutron grafik eye scene "
            } else if (zoneTypeid == 2) {
            	device = addChildDevice(app.namespace, "Lutron Dimmer", dni, null, ["label":"${atomicState.zones[dni].name}" ?: "Lutron Dimmer"])
                log.debug "Created ${device.displayName} with id $dni as a lutron dimmer"
            } else {
            	device = addChildDevice(app.namespace, "Lutron switch", dni, null, ["label":"${atomicState.zones[dni].name}" ?: "Lutron switch"])   	
                log.debug "Created ${device.displayName} with id $dni as a lutron switch"
			}
        } else {
            log.warn "found ${device.displayName} with id $dni already exists"
        }
    }
    log.trace "Created/Found ${zones.size()} lutron zones."
}

def deleteZoneDevices() {
	log.info "Entered Method: deleteZoneDevices()"
    
    // Delete any zones that are no longer in settings
    def delete = []
    if(!lutronZones) {
		log.debug "Delete all zones"
        delete = getAllChildDevices() 
	} else {
    	log.debug "Get all child zone(s) not selected in App settings"
    	delete = getChildDevices().findAll { !lutronZones.contains(it.deviceNetworkId)}
    }
	log.warn "Delete: " + delete ?: 'N/A' + ", deleting " + delete.size() ?: 0 + " zones"
    delete.each {deleteChildDevice(it.deviceNetworkId) } 
}

def sendCmd(cmd,zone,level){
    log.info "Entered Method: sendCmd(${cmd}, ${zone}, ${level})"

	try {
		def httpRequest = [
			method: "GET",
			path: getPlatformUri() + "/command/$cmd/zone/$zone/level/$level",
			headers:	[
				HOST: getHostAddress(),
				"Content-Type": "application/json",                        
			]
		]
		
		sendHubCommand(new physicalgraph.device.HubAction(httpRequest, null, [callback: sendCmdCallBack]))
	} catch (all) {
		log.error "Cannot connect to the Raspberry PI API services gateway. Message: " + all
	}
}

def sendCmdCallBack(hubResponse) {
	log.info "Entered Method: sendCmdCallBack(${hubResponse})"
    
    try {
		def description = hubResponse.description
		def msg = parseLanMessage(description)

		def status = msg.status          // => http status code of the response
		def json = msg.json              // => any JSON included in response body, as a data structure of lists and maps

		log.debug "lanRequest status response: $status" 
		if (status == 200) {
        	log.warn "Raspberry PI API returned 200"
		} else {
			log.error "Not a 200 Response from the Raspberry PI API services gateway"
		}
	} catch (all) {
		log.error "No response from the Raspberry PI API services gateway. Message: " + all
	}
}

def on(childDevice, transition_deprecated = 0) {
    log.info "Entered Method: on(${childDevice})"
   	
    def percent = childDevice.device?.currentValue("level") as Integer
    log.debug "Device Level: " + percent
    
    def childDeviceNetworkId = childDevice.device.deviceNetworkId
    if (percent == 0) {
    	sendCmd('SDL', childDeviceNetworkId.split(/\./).last(), 100)
    	sendEvent(childDeviceNetworkId, [name: "switch", value: "on"])
        sendEvent(childDeviceNetworkId, [name: "level", value: "100"])
    } else {
    	sendCmd('SDL',childDeviceNetworkId.split(/\./).last(), percent)
        sendEvent(childDeviceNetworkId, [name: "switch", value: "on"])
    }
}

def off(childDevice, transition_deprecated = 0) {
   	log.info "Entered Method: off(${childDevice})"

	def childDeviceNetworkId = childDevice.device.deviceNetworkId
    sendCmd('SDL', childDeviceNetworkId.split(/\./).last(), 0)
    sendEvent(childDeviceNetworkId, [name: "switch", value: "off"])
}

def setLevel(childDevice, percent) {
   	log.info "Entered Method: setLevel(${childDevice}, ${percent})"

   	sendCmd('SDL', childDevice.device.deviceNetworkId.split(/\./).last(), percent)
	
    def childDeviceNetworkId = childDevice.device.deviceNetworkId
    sendEvent(childDeviceNetworkId, [name: "level", value: "$percent"])
    
    // If light level is 0 then send turn off switch event
    if (percent == 0) {
    	sendEvent(childDeviceNetworkId, [name: "switch", value: "off"])
    } else {
    	sendEvent(childDeviceNetworkId, [name: "switch", value: "on"])
    }
}

def pollZones(){
    log.info "Entered Method: pollZones()"
	
    try {
		def httpRequest = [
			method: "GET",
			path: getPlatformUri() + "/zones/",
			headers:	[
				HOST: getHostAddress(),
				"Content-Type": "application/json",                        
			]
		]
		
		def hubAction = new physicalgraph.device.HubAction(httpRequest, null, [callback: pollCallbackHandler])
        sendHubCommand(hubAction)
	} catch (all) {
		log.error "Cannot connect to the Raspberry PI API services gateway. Message: " + all
	}
    return
}

def pollCallbackHandler(hubResponse) {
	log.info "Entered Method: pollCallbackHandler"
    log.info "Hub Response: " + hubResponse
    
    // try {
		def description = hubResponse.description
		def msg = parseLanMessage(description)

		def status = msg.status          // => http status code of the response
		def json = msg.json              // => any JSON included in response body, as a data structure of lists and maps

		log.debug "lanRequest status response: $status" 
		if (status == 200) {
			def zones = [:]
            
			json.each {zone ->
				def dni = [app.id, zone.zone].join('.')
				zones[dni] = [
					name : zone.name,
					zonetypeid : zone.zonetype_id,
                    zonetype : zone.zonetype,
					system : zone.system,
					level : 0,
					state : zone.state]
			}

			atomicState.zones = zones
            
			// Get all child devices
    		def devices = getChildDevices()
            
            devices.each { child ->
            	def childDeviceNetworkId = child.device.deviceNetworkId
            	def childDevice = atomicState.zones[childDeviceNetworkId].name
                def lutronState = atomicState.zones[childDeviceNetworkId].state
                def smartthingsState = child.currentState("switch")?.value
                
                if ((lutronState != null) && (lutronState != smartthingsState)) {
                	log.debug "Child device: ${childDevice}, Lutron State: ${lutronState}, Smartthing State: ${smartthingsState}"

                	if (smartthingsState == "on") {
                    	log.debug "Send ${childDevice} Switch On message"
                    	sendEvent(childDeviceNetworkId, [name: "switch", value: "off"])                  
                	} else if (smartthingsState == "off") {
                    	log.debug "Send  ${childDevice} Switch Off message"
                    	sendEvent(childDeviceNetworkId, [name: "switch", value: "on"]) 
                	}
            	}
            }
    	} else {
			log.error "Not a 200 Response from the Raspberry PI API services gateway"
		}
	/* } catch (all) {
		log.error "No response from the Raspberry PI API services gateway. Message: " + all
	}*/
}