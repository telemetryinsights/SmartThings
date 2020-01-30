# RadioRA Classic Smart Bridge

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

REST server for controlling Lutron RadioRA Classic light switches and dimmers (this original Lutron lighting system is also called RadioRA 1 or Legacy RadioRA). The RadioRA Classic Smart Bridge must by run on a system (such as a Raspberry Pi) with a physical RS232 serial connection to one of Lutron's RadioRA Classic hardware serial modules such as the RA-RS232 or Chronos RA-SBT-CHR.

Credit goes to Stephen Harris at Homemations for developing this Python-based Lutron RadioRA Classic server.

## Configuration

1. Using your Lutron RadioRA Classic RS232 module, you must physically assign each Zone to a specific switch or dimmer. See the manual for your Lutron hardware module for these steps. Any Zones that are not physically configured on the Lutron hardware device will show up as Unassigned when querying zones later.

2. Connect the RS-232 module to the host that will be running the RadioRA Classic Smart Bridge with a serial cable. The Bridge should auto-discover the RadioRA Classic RS-232 hardware, but if it does not you can set the environment variable RADIORA_BRIDGE_TTY to the /dev/tty device which maps to your serial port.

3. Start the RadioRA Classic Smart Bridge (execute ./run.sh in simple case; or use the provided Docker container)

4. Using your browser, access http://yourhost:8333/api/ to display info on the supported APIs.

NOTE: A zone is any individual RadioRA Classic dimmer, switch, GRAFIK Eye Interface, or Sivoia Control. Each RadioRA Classic system has a maximum of 32 zones. Multiple instances of the RadioRA Classic Bridge can be run on different ports with serial cables connected to different RadioRA hardware modules to support an unlimited number of zones.

## Required Hardware

* Raspberry Pi or other server to run the RadioRA Classic Smart Bridge

* Lutron hardware module that supports RS-232 communication with a RadioRA Classic system:

    - [RadioRA RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf) (RA-RS232)
    - [RadioRA Chronos System Bridge](http://www.lutron.com/TechnicalDocumentLibrary/044037b.pdf) (RA-SBT-CHR)

* USB to male RS232 serial cable (or direct wire to Raspberry Pi GPIO pins using a MAX3232 RS-232 male adapter)

## Configuration

1. Install the RadioRA Classic Smart Bridge on your Raspberry Pi or other server machine (Docker container is also provided)

NOTE: If you want to integrate the Smart Bridge with SmartThings (vs using it standalone for developing your own code against the REST API), complete the following:

## Examples

```
wget http://localhost:8333/api/zones/
```

```json
[
  {
    "id": 1,
    "name": "Zone 1",
    "zone": 1,
    "system": 1,
    "state": "on",
    "zonetypeid": 2,
    "zonetype": "Dimmer"
  },
  {
    "id": 2,
    "name": "Zone 2",
    "zone": 2,
    "system": 1,
    "state": "on",
    "zonetypeid": 2,
    "zonetype": "Dimmer"
  },
  {
    "id": 3,
    "name": "Zone 3",
    "zone": 3,
    "system": 1,
    "state": "off",
    "zonetypeid": 2,
    "zonetype": "Dimmer"
  },
  ...
]
```

### NOTES

* the RadioRA Classic serial APIs provided by Lutron have no way to read the current dimmer level, only on/off state
* does not support native 15 Phantom Buttons or Room/Scene features of the Lutron hardware modules
* does not support fade time for dimmer state changes
* does not support setting LED lights on other master controls
* there is no security for the port, anyone with access can control the lights

### FUTURE

- support Phantom Buttons to control groups of zones (faster setting entire groups than individual one-by-one zone turning on/off) ... or use one of the Phantom Buttons to specify which lights should flash for alarms

- SGS command support for Set GRAFIK Eye Scene (applies to GRAFIK Eye Interfaces and Sivoia Controls)

- remember the previous dimmer level settings, use as defaults for on if not configured

- support for asynchronous ZMP zone monitoring (with ZMPMON / ZMPMOFF support) ... Constantly monitor RS232 for status updates...note in manual: "If an external RS232 system is not setup to continuously monitor the RS232 port, asking the RadioRA System for status is a useful way to monitor RadioRA System actions or get an updated status. However, using the Serial Device in this manner will cause you to miss MBP commands (Master Control Button Press) and LZC commands (Local Zone Change)."
