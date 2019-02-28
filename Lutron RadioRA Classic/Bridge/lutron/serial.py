import os
import time
import serial
import logging

log = logging.getLogger(__name__)

# unless an explicit SERIAL_TTY is specified to use, this searches by default across
# a set of common TTYs to find a RadioRA Classic RS232 module
DEFAULT_SERIAL_TTYS_TO_SEARCH = [ '/dev/ttyS0',         # Raspberry Pi mini UART GPIO
                                  '/dev/ttyAMA0',       # Raspberry Pi GPIO pins 14/15 (pre-Bluetooth RPi 3)
                                  '/dev/serial0',       # RPi 3 serial port alias 1
                                  '/dev/serial1',       # RPi 3 serial port alias 2
                                  '/dev/tty.usbserial', # typical MacOS USB serial adapter
                                  '/dev/ttyUSB0',       # Linux USB serial 1
                                  '/dev/ttyUSB1',       # Linux USB serial 2
                                  '/dev/ttyUSB2'        # Linux USB serial 3
                                ]

class RadioRASerial:

    def __init__(self):
        self.tty_timeout = int(os.environ['SERIAL_TTY_TIMEOUT']) if 'SERIAL_TTY_TIMEOUT' in os.environ else 1
        ttys_to_search = DEFAULT_SERIAL_TTYS_TO_SEARCH

        # NOTE: SERIAL_TTY environment variable overrides the default search paths
        if 'SERIAL_TTY' in os.environ:
            tty_config = os.environ['SERIAL_TTY']
            print(">>>>> RadioRA Classic device search paths overridden by env variable SERIAL_TTY=" + tty_config)
            ttys_to_search = ','.split(tty_config)

        self.__discover_radiora_serial__(ttys_to_search)

    def __discover_radiora_serial__(self, ttys_to_search):
        print(">>>>> Discovering RadioRA device on serial interfaces: {}".format(', '.join(ttys_to_search)))
        for tty in ttys_to_search:
            try:
                if not os.path.exists(tty):
                    print(">>>>>    Serial device {} does not exist, ignoring".format(tty))
                    continue
                
                self.serial = serial.Serial(tty,
                                            baudrate=9600, # 9600 baud is required by RA-RS232
                                            parity=serial.PARITY_NONE,
                                            stopbits=serial.STOPBITS_ONE,
                                            bytesize=serial.EIGHTBITS,
                                            dsrdtr=True, rtscts=True,
                                            timeout=self.tty_timeout)
                self.writeCommand('VERI')
                response = self.readData()

                # response = REV,M<Master Revision>,S<Slave Revision>, e.g. REV,M3.14,S1.01
                if ((response != None) and response.startswith('REV,')):
                    self.version = response.lstrip('REV,')
                    self.tty = tty
                    print('>>>>> Discovered Lutron RadioRA Classic at {} (version={})'.format(self.tty,self.version))
                    break

                self.serial.close()
                self.serial = None

            except:
                print('Unexpected error: ', sys.exc_info()[0])
                raise RuntimeError("No RadioRA RS232 devices discovered at {}".format(', '.join(ttys_to_search)))
        
        if self.version == None:
            raise RuntimeError("No RadioRA RS232 devices discovered at {}".format(', '.join(ttys_to_search)))

    def __repr__(self):
        return '<RadioRA Classic RS232 : tty={} : version={}>'.format(self.tty, self.version)

    def _readline(self):
        eol = b'\r'
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.serial.read(1)
            if c:
                if c == eol:
                    #line += '|'
                    break
                line += c
            else:
               break
        return bytes(line).decode('utf-8')

    def writeCommand(self, command):
        print('>>>>> Serial write: {}'.format(command))
        self.serial.reset_input_buffer()
        self.serial.write((command + "\r\n").encode('utf-8'))

    # not the most efficient reading one byte at a time, but it is way faster than
    # waiting for a 1 or 2 second timeout on every read. This could be improved in future.
    def readData(self):
        start = time.time()
        result = result = self._readline()
        while self.serial.in_waiting:
            result = result + _readline(ser)
            result = result.decode('utf-8').upper()
        end = time.time()

        print('>>>>> Serial read ({1:.0f} ms): {0}'.format(result, 1000 * (end-start)))
        return result