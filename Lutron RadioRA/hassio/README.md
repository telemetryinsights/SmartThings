# lutron-radiora1

[Lutron](http://lutron.com/) RadioRA V1 SmartThings Gateway (Hass.io)

This integrates Lutron's RadioRA (original version 1) light switches and zones with
Home Assistant by packaging up
[Homemation's Lutron RadioRA Manager](https://github.com/homemations/SmartThings)
into a [Hassio](https://www.home-assistant.io/hassio/) add-on. Note that this requires
Home Assistant 0.87 or later as it relies on native SmartThings integration (rather than
the added complexity of a MQTT bridge).

Provides integration of a Lutron RadioRA 1 home lighting system into the SmartThings platform via a Raspberry PI Gateway. The Raspberry PI Gateway was developed by HomeMations using Python to expose RESTful APIs. The Raspberry PI connects to the Lutron RadioRA 1 serial interface (part #RA-RS232) and home LAN to bridge communication
from the SmartThings hub to the RS232 interface.

Thanks to Stephen Harris <stephen@homemations.com> for implementing the RadioRA 1 Gateway.

= Required Hardware =

* Lutron's [RadioRA RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf)
* Raspberry Pi capable of running [Hassio](https://www.home-assistant.io/hassio/)
* RS232 Serial interface to Pi: direct wire RadioRA RA-S232 to Pi pins *OR* a USB serial adapter

See the [Homemation Lutron RadioRA Manager](https://github.com/homemations/SmartThings)
project for details on hardware setup, SmartThings groovy script installs, as well as what features
are supported. Note, the initial Lutron RadioRA Manager release only supports dimmers, switches and zones.

## FIXME

- FLASK_SERVER_NAME: 192.168.1.142:8080 (see python/settings.py)
- where do logs go?

## Hassio Setup

1. In your Hass.io "Add-On Store", add the repository URL to the Lutron RadioRA HASSIO add-on:

<pre>
     https://github.com/rsnodgrass/lutron-radiora1/
</pre>

2. Find the "Lutron RadioRA Manager" in the add-ons and install it

3. Follow Homemation's instructions on how to add the SmartApp and DeviceType in
   SmartThings.

### Configuration

Change the config of the app in hassio then edit the configuration.yaml:

<pre>switches:
  - platform: mqtt
    name: "Lutron RadioRA"
</pre>

Add the following to the configuration.yaml for each switch:

<pre>
  - platform: mqtt
    name: "Kitchen Door"
    state_topic: "adt/zone/Kitchen Door/state"
    device_class: door
    retain: true
    value_template: '{{ value_json.status }}' 
</pre>
