import serial
import time
from serial import SerialException


def extract_second_value(data_str):
    """Extract data from string returned by device"""
    items = data_str.split(',')
    if len(items) >= 2:
        result = items[1].strip()
        if result == 'NoProbe':
            return -2
        return result
    return -1


class WikaTempProbe:
    def __init__(self, com):
        """Requires to specify which COM port is Wika device connected"""
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 9600
        self.serial_port.parity = serial.PARITY_NONE
        self.serial_port.bytesize = serial.EIGHTBITS
        self.serial_port.stopbits = serial.STOPBITS_ONE
        self.serial_port.xonxoff = False
        self.serial_port.rtscts = False
        self.serial_port.dsrdtr = False
        self.serial_port.timeout = None
        self.serial_port.timeout = 1.0
        self.serial_port.port = com

    def connect(self):
        """Opens connection to the Wika device"""
        try:
            self.serial_port.open()
            self.set_system_remote(True)
            return True
        except (SerialException, IOError, ValueError) as e:
            print("temp probe: ", e)
            return False

    def disconnect(self):
        """Closes connection with Wika device"""
        try:
            self.set_system_remote(False)
            self.serial_port.close()
        except (SerialException, IOError, ValueError) as e:
            print(e)

    def ident(self):
        """Returns identifications name and serial number"""
        scpi_command = '*IDN?'
        ident = self._send_command(scpi_command, 1.0)
        return ident

    def set_unit_celsius(self):
        """Sets unit to celsius"""
        scpi_command = 'UNIT:TEMP? CEL'
        self._send_command(scpi_command)

    def measure_channel(self, ch):
        """Reads measured temprature from probe's channel"""
        mapping = {'A': 1, 'B': 2}
        try:
            scpi_command = f'MEASURE:CHANNEL? {mapping[ch]}'
            return extract_second_value(self._send_command(scpi_command))
        except Exception as e:
            print(e)
            return -1

    def set_system_remote(self, system):
        """Sets probe to the remote or local mode disabling keypads
        True -> REMOTE
        False -> LOCAL
        """
        sys = 'REMOTE' if system else 'LOCAL'
        scpi_command = f'SYSTEM:{sys}'
        self._send_command(scpi_command)

    def _send_command(self, command, sleep=0.666):
        """Sends command to the Wika probe"""
        try:
            if self.serial_port.isOpen():
                self.serial_port.reset_input_buffer()
                for byte in (command + '\r').encode():
                    self.serial_port.write(bytearray([byte]))
                    time.sleep(0.025)
                # self.serial_port.write((command + '\r\n').encode())
                time.sleep(sleep)
                res = self.serial_port.read_all()
                response = res.decode().strip()
                return response
            else:
                print("PORT IS NOT OPEN")
                return -1
        except Exception as e:
            print(e)
            return -1


# temp_probe = WikaTempProbe('COM3')
# temp_probe.connect()
# res = temp_probe.measure_channel('B')
# temp = None
# if res == -1:
#     print("ERROR")
# elif res == -2:
#     print("Wrong Channel Selected")
# else:
#     temp = float(res)
# print(temp)
# temp_probe.disconnect()

