# RadioRA Classic Smart Bridge

REST server for controlling Lutron RadioRA Classic light switches and dimmers (this original Lutron lighting system is also called RadioRA 1 or Legacy RadioRA). The RadioRA Classic Smart Bridge must by run on a system (such as a Raspberry Pi) with a physical RS232 serial connection to one of Lutron's RadioRA Classic hardware serial modules such as the RA-RS232 or Chronos RA-SBT-CHR.

Credit goes to Stephen Harris at Homemations for developing this Python-based Lutron RadioRA Classic server.

## Required Hardware

* Lutron hardware module that supports RS-232 communication with a RadioRA Classic system:
    - [RadioRA RS232 Serial Interface](http://www.lutron.com/TechnicalDocumentLibrary/044005c.pdf) (RA-RS232)
    - [RadioRA Chronos System Bridge](http://www.lutron.com/TechnicalDocumentLibrary/044037b.pdf) (RA-SBT-CHR)
* Raspberry Pi or other server to run the Bridge
* RS232 serial cable (or direct wire to Raspberry Pi GPIO pins using a MAX3232 RS-232 male adapter)

## Configuration

No special configuration is necessary to start the RadioRA Classic Smart Bridge in a very basic operational mode.
It starts up on port 8333 and immediately can accept requests to control any of the 32 switches/dimmers.

>>> Actually, you have to assign dimmer or switch to each of the 32 zones!

### FUTURE

- support Phantom Buttons to control groups of zones (faster if setting entire groups than individual one-by-one zone turning on/off)

- An SDL command (Set Dimmer Level) applies to Dimmers, an SSL command (Set Switch Level) applies to Switches, and an SGS command (Set GRAFIK Eye Scene) applies to GRAFIK Eye Interfaces and Sivoia Controls.

- See if we can auto-discover what lights are configured with ALL ON, poll for state, then ALL OFF.

- Expose FLASH mode for allowing alarm systems to trigger flashing lights

- Constantly monitor RS232 for status updates...note in manual: "If an external RS232 system is not setup to continuously monitor the RS232 port, asking the RadioRA System for status is a useful way to monitor RadioRA System actions or get an updated status. However, using the Serial Device in this manner will cause you to miss MBP commands (Master Control Button Press) and LZC commands (Local Zone Change)."

- Support for GRAFIK Eye and Sivoia control units (including scenes)