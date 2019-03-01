# RadioRA Classic Bridge Changelog

### 1.2 / 2019-02-28
RadioRA Classic Smart Bridge now auto-discovers the serial tty of the RS232 hardware module for common cases.

 - updated documentation
 - split out SmartThings specific code into SmartThings/ subfolder
 - now auto-discovers the RadioRA RS232 hardware by probing a set of common serial ttys
 - configurable serial port discovery list via SERIAL_TTY environment variable (if needed)
 - emits the Lutron version of the RS232 hardware in logs

### 1.1 / 2019-02-25
Added documentation, updated interfaces and performance improvements

 - significant refactoring and simplification to make install easier
 - support for turning flash on/off for all lights (for alarm integration)
 - significant RS232 read performance improvement 
 - removed CRUD interfaces for modifying zonetypes
 - security issues starting to be addresses
 - defaulted the name of the zones to "Zone 1" through "Zone 32" as the out of the box configuration
 - defaulted each zone to be dimmer switches 'out of the box'
 - port switched to a less common port 8333 to avoid potential conflicts with other services running at 8080 (not an issue with Docker, but might as well change)
 - Docker support for running Bridge as a container (allows running on lots of different hardware types)
 - first round of documentation added

### 1.0
Initial release by Stephen Harris at Homemations
