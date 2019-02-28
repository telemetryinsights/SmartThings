# RadioRA Classic Smart Bridge

REST server for controlling Lutron RadioRA Classic light switches and dimmers (this original Lutron lighting system is also called RadioRA 1 or Legacy RadioRA). The RadioRA Classic Smart Bridge must by run on a system (such as a Raspberry Pi) with a physical RS232 serial connection to one of Lutron's RadioRA Classic hardware serial modules such as the RA-RS232 or Chronos RA-SBT-CHR.

Credit goes to Stephen Harris at Homemations for developing this Python-based Lutron RadioRA Classic server.

## Configuration

1. Using your Lutron RadioRA Classic RS232 module, you must physically assign each Zone to a specific switch or dimmer. See the manual for your Lutron hardware module for these steps. Any Zones that are not configured on the hardware device will show up as Unassigned when querying zones later.

2. Connect the RS-232 module to the host that will be running the RadioRA Classic Smart Bridge with a serial cable. The Bridge should auto-discover the RadioRA Classic RS-232 hardware, but if it does not you can set the environment variable SERIAL_TTY to the /dev/tty device which maps to your serial port.

3. Start the RadioRA Classic Smart Bridge (execute ./run.sh in simple case; or use the provided Docker container)

4. Use your browser to go to http://<yourhosthere>:8333/api/

NOTE: A zone is any individual RadioRA Classic dimmer, switch, GRAFIK Eye Interface, or Sivoia Control. Each RadioRA Classic system has a maximum of 32 zones. Multiple instances of the Bridge can be run on different ports with serial cables connected to different RadioRA hardware modules to support an unlimited number of zones.
