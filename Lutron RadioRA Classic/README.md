# Lutron RadioRA Classic Tools

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Tools for integrating with Lutron RadioRA Classic light switches and dimmers including a REST-RS232 bridge plus additional optional SmartThings scripts. Credit goes to Stephen Harris at Homemations for developing this Python-based Lutron RadioRA Classic RESTful server and SmartThings scripts.

### RadioRA Classic Smart Bridge

RESTful server for controlling lighting switches and dimmers for Lutron's RadioRA Classic system (this original Lutron lighting system is also called RadioRA 1 or Legacy RadioRA). The RadioRA Classic Smart Bridge must by run on a system (such as a Raspberry Pi) with a physical RS232 serial connection to one of Lutron's RadioRA Classic hardware serial modules such as the RA-RS232 or Chronos RA-SBT-CHR.

See [Bridge/ sub-directory](Bridge/) for instructions on setting up the RadioRA Classic Smart Bridge.

### SmartThings Setup

See [SmartThings/ sub-directory](SmartThings/) for the Groovy scripts that must be installed for your SmartThings hub which integrate your RadioRA Classic Smart Bridge into SmartThings.
