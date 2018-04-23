/** 
 *  iSpy PTZ Camera 
 *  Image Capture and Video Streaming courtesy Stephen Harris (stephen@homemations.com) 
 *   
 *  Copyright 2016 Homemations, Inc. 
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
	definition (name: "iSpy PTZ Camera", namespace: "homemations", author: "Stephen Harris") {
		capability "Image Capture"
		capability "Sensor"
		capability "Switch"
        capability "Switch Level"
        capability "Refresh"
        capability "Notification"
        capability "Configuration"
		capability "Video Camera"
		capability "Video Capture"
           
        command "start"
		command "stop"
        command "left"
		command "right"
		command "up"
		command "down"
        command "home"
        command "zoomIn"
        command "zoomOut"
        command "camOn"
        command "camOff"
        command "vidOn"
        command "vidOff"
	}    

	mappings {
   		path("/getInHomeURL") {
       		action: [GET: "getInHomeURL"]
   		}
	}
    
    tiles (scale: 2){
    	multiAttributeTile(name: "videoPlayer", type: "videoPlayer", width: 6, height: 4, canChangeIcon: true, inactiveLabel: true, canChangeBackground: false) {
			tileAttribute("device.switchVideo", key: "CAMERA_STATUS") {
				attributeState("on", label: "Active", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", action: "vidOff", backgroundColor: "#79b821", defaultState: true)
				attributeState("off", label: "Inactive", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", action: "vidOn", backgroundColor: "#ffffff")
				attributeState("restarting", label: "Connecting", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", backgroundColor: "#53a7c0")
				attributeState("unavailable", label: "Unavailable", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", action: "refresh.refresh", backgroundColor: "#F22000")
			}

            tileAttribute("device.errorMessage", key: "CAMERA_ERROR_MESSAGE") { 
                attributeState("errorMessage", label: "", value: "", defaultState: true) 
            } 
            
            tileAttribute("device.camera", key: "PRIMARY_CONTROL") {
				attributeState("on", label: "Active", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", backgroundColor: "#79b821", defaultState: true)
				attributeState("off", label: "Inactive", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", backgroundColor: "#ffffff")
				attributeState("restarting", label: "Connecting", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", backgroundColor: "#53a7c0")
				attributeState("unavailable", label: "Unavailable", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", backgroundColor: "#F22000")
			}         

			tileAttribute("device.startLive", key: "START_LIVE") {
				attributeState("live", action: "start", defaultState: true)
			}

			tileAttribute("device.stream", key: "STREAM_URL") {
				attributeState("activeURL", defaultState: true)
			}
			
            tileAttribute("device.betaLogo", key: "BETA_LOGO") {
				attributeState("betaLogo", label: "", value: "", defaultState: true)
			}
        }
    	
        standardTile("left", "device.switch") {
			state "left", label: "Left", action: "left", nextState: "moving", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowLeft.png"
            state "moving", label: "moving", action:"", backgroundColor: "#53a7c0", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowLeft.png"
		}
        
        standardTile("up", "device.switch") {
			state "up", label: "Up", action: "up", nextState: "moving", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowUp.png"
            state "moving", label: "moving", action:"", backgroundColor: "#53a7c0", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowUp.png"
		}
         
        standardTile("down", "device.switch") {
			state "down", label: "Down", action: "down", nextState: "moving", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowDown.png"
            state "moving", label: "moving", action:"", backgroundColor: "#53a7c0", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowDown.png"
        }      
        
        standardTile("right", "device.switch") {
			state "right", label: "Right", action: "right", nextState: "moving", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowRight.png"
            state "moving", label: "moving", action:"", backgroundColor: "#53a7c0", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/arrowRight.png"
		}
        
        standardTile("zoomIn", "device.switch") {
			state "in", label: "In", action: "zoomIn", nextState: "zoom", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/zoomIn.png"
            state "zoom", label: "Zoom", action:"", backgroundColor: "#53a7c0", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/zoomIn.png"
        }      
        
        standardTile("zoomOut", "device.switch") {
			state "out", label: "Out", action: "zoomOut", nextState: "zoom", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/zoomOut.png"
            state "zoom", label: "Zoom", action:"", backgroundColor: "#53a7c0", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/zoomOut.png"
		}
        
	    standardTile("camera", "device.image") {
            state "default", label: "", action: "", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/genericCameraPTZ-icn.png", backgroundColor: "#FFFFFF"
        }

        carouselTile("cameraDetails", "device.image", width: 3, height: 2) { }

        standardTile("take", "device.image", width: 2, height: 2, inactiveLabel: true, canChangeBackground: false) {
            state "take", label: "Take", action: "Image Capture.take", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/snapShot.png", backgroundColor: "#FFFFFF", nextState:"taking"
            state "taking", label:'Taking', action: "", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/snapShot.png", backgroundColor: "#53a7c0"
            state "image", label: "Take", action: "Image Capture.take", icon: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/snapShot.png", backgroundColor: "#FFFFFF", nextState:"taking"
        }
        
        standardTile("cam", "device.switch") {
            state "on", label:'${currentValue}', action:"camOff", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/videoOn.png", backgroundColor:"#79b821"
            state "off", label:'${currentValue}', action:"camOn", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/videoOff.png", backgroundColor:"#ffffff"
		}
        
       standardTile("vid", "device.switch") {
            state "on", label:'${currentValue}', action:"vidOff", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/videoRecordOn.png", backgroundColor:"#79b821"
            state "off", label:'${currentValue}', action:"vidOn", icon:"https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/videoRecordOff.png", backgroundColor:"#ffffff"
		}
        
        main "videoPlayer"
        details(["videoPlayer", "videoStart", "left", "up", "down", "right", "zoomIn", "zoomOut", "cameraDetails", "take", "cam", "vid" ])  
	}
}

// Smart Things standard device handler functions section
def installed(){ 
	log.debug "Device In Function: installed()"
    
     // The device refreshes every 5 minutes by default so if we miss 2 refreshes we can consider it offline
    // Using 12 minutes because in testing, device health team found that there could be "jitter"
	sendEvent(name: "checkInterval", value: 60 * 12, data: [protocol: "cloud"], displayed: false)
}

def updated(){ 
	log.debug "In Function: updated()"
  	configure() 
}

// Device Command functions section
def start() {    
    log.debug "In Function: start"
       
    def dataLiveVideo = [ 
		OutHomeURL  : getVideoAPIURL(parent.getStreamPath(), false),
		InHomeURL   : getVideoAPIURL(parent.getStreamPath(), true), 
		ThumbnailURL: "https://s3-us-west-1.amazonaws.com/iriesolutions/SmartThings/icons/iSpy/securityCam.png", 
		cookie      : [key: "key", value: "value"] 
	] 
 
    def event = [ 
        name           : "stream", 
        value          : groovy.json.JsonOutput.toJson(dataLiveVideo).toString(), 
        data		   : groovy.json.JsonOutput.toJson(dataLiveVideo), 
        descriptionText: "Starting the livestream", 
        eventType      : "VIDEO", 
        displayed      : true, 
        isStateChange  : true 	
    ] 
	
    sendEvent(event)
}

def stop() { 
    log.debug "In Function: stop"
    
    poll()
}

def take() {
   	log.debug "In Function: takePicture()"
    
    def imageBytes
    httpGet(getAPIParams(parent.getSnapShot(), null, false), { response -> imageBytes = response.data })
    
    if (imageBytes) {
        storeImage(getPictureName(), imageBytes)
        return true
    } else {
    	return false
    }
}

def camOn() {
    log.debug "In Function: on()  - Turning camera on"
   
    def ptzCmd = [cmd: "switchon", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
    sendEvent(name: "switch", value: "on")
}

def camOff() {
    log.debug "In Function: off() - Turning camera off"

    def ptzCmd = [cmd: "switchoff", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
    sendEvent(name: "switch", value: "off")
}

def vidOn() {
    log.debug "In Function: vidOn() - Turning video recording on"
   
    // ot = Object type; 1 for Microphone, 2 for camera
    // Turn on recording that the specific object camera on iSpyConnect in addition to viewing on SmartThings
    def ptzCmd = [cmd: "record", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
    sendEvent(name: "switch", value: "on")
}

def vidOff() {
    log.debug "In Function: vidOff() - Turning video recording off"

    // ot = Object type; 1 for Microphone, 2 for camera
    // Turn on recording that the specific object camera on iSpyConnect in addition to viewing on SmartThings
    def ptzCmd = [cmd: "recordstop", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
    sendEvent(name: "switch", value: "off")
}


def up() {
    log.debug "In Function: up"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_3", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def left() {
    log.debug "In Function: left"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_1", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def right() {
    log.debug "In Function: right"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_5", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def down() {
     log.debug "In Function: down"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_7", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def zoomIn() {
	log.debug "In Function: zoomIn"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_9", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def zoomOut() {
	log.debug "In Function: zoomOut"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_10", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def home() {
    log.debug "In Function: home"
    
    def ptzCmd = [cmd: "ptzcommand", field: "ptz", value: "ispydir_11", ot: "2"]
    httpGet(getAPIParams(parent.getCameraPath(), ptzCmd, false), { response -> response?.data })
}

def presetOne() {
    log.debug "In Function: presetOne"
    
    moveCmd("preset=move,100")
}

def presetTwo() {
    log.debug "In Function: presetTwo"
    
   	moveCmd("preset=move,101")
}

def presetThree() {
    log.debug "In Function: presetThree"
    
    moveCmd("preset=move,102")
}

// Smart App with Child devices functions section
def ping() {
	// Device Watch will ping the device to proactively determine if the device has gone offline
	// If the device was online the last time we refreshed, trigger another refresh as part of the ping.
	log.debug "Device In Function: ping()"
    
    def isAlive = device.currentValue("deviceAlive") == "true" ? true : false
    if (isAlive) {
        refresh()
    }
}

void poll() {
	log.debug "Device In Function: poll()"
    log.debug "Executing 'poll' using parent SmartApp"
	parent.pollChild()
}

// Utility functions section
private getVideoAPIURL(pathAPI, inHome) {
	log.debug "In Function: getAPIURL"
    
    // Retrieve server configuration data from parent App
    def server = parent.getAtomicStateServer()
    log.debug "Server: ${server}"
    
    // Get the iSpyConnect deviceID
    def deviceId = device.deviceNetworkId.split(/\./).last()
    
    // Build server URI based on if SSL is/not in use
    def serverURI = null
    if (!server.ssl) {
    	serverURI = "http://"
    } else {
    	serverURI = "https://"
    }
    
    // Append the host IP and port based on in/out home based on connection via INTRANET/INTERNET
    if (inHome) {
    	serverURI = serverURI + server.lan
    } else {
    	serverURI = serverURI + server.wan
    }
    
    // Complete full URI for API call to the end point
    def APIURL = serverURI + pathAPI + "?auth=" + server.auth + "&oid=" + deviceId
    log.debug "APIURL: ${APIURL}"
    
    return APIURL
}

private getAPIParams(pathAPI, def addQuery = [:], inHome) {
	log.debug "In Function: getAPIURL(${pathAPI}, ${addQuery}, ${inHome})"
    
    // Retrieve server configuration data from parent App
    def server = parent.getAtomicStateServer()
    log.debug "Server: ${server}"
    
    // Get the iSpyConnect deviceID
    def deviceId = device.deviceNetworkId.split(/\./).last()
    
    // Build server URI based on if SSL is/not in use
    def serverURI = null
    if (!server.ssl) {
    	serverURI = "http://"
    } else {
    	serverURI = "https://"
    }
    
    // Append the host IP and port based on in/out home based on connection via INTRANET/INTERNET
    if (inHome) {
    	serverURI = serverURI + server.lan
    } else {
    	serverURI = serverURI + server.wan
    }
       
    def query = [auth: server.auth, oid: deviceId]
    if (addQuery != null) {
    	query = query + (addQuery)	
    } 
    
    // Complete full URI for API call to the end point
    def params = [ 	uri: serverURI,
    				path: pathAPI,
                    query:  query
    ]
    log.debug "API Params: ${params}"
    
    return params
}

private getInHomeURL() { 
    log.debug "In Function: getInHomeURL()"
    
    // Build API URL for video streaming command for the in home URI INTRANET facing end point
    [InHomeURL: getVideoAPIURL(parent.getStreamPath(), true)] 
}

private getPictureName() {
    def pictureUuid = java.util.UUID.randomUUID().toString().replaceAll('-', '')
    getCameraUuid() + "_$pictureUuid" + ".jpg"
}

private getCameraUuid() {
    // Get the iSpyConnect deviceID
    def deviceId = device.deviceNetworkId.split(/\./).last()
}