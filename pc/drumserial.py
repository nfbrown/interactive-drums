import serial
from serial.tools import list_ports
from sys import platform as _platform


class DrumSerial:
    serial_port = serial.Serial()

    def __init__(self):
        self.serial_port.baudrate = 115200
        self.serial_port.timeout = 5
        com_ports = list_ports.comports()
        if _platform == "linux" or _platform == "linux2":
            filtered = [p[0] for p in com_ports
                        if str(p[0]).startswith('/dev/ttyUSB')]
            self.serial_port.port = filtered[0]
        elif _platform == "darwin":
            print _platform + ' currently not supported'
            # Uncomment the following three lines to support Mac
            # Note getting the GUI to run on Mac will require additional
            # configuration
            # filtered = [p[0] for p in com_ports
            #             if str(p[0]).startswith('/dev/cu.usbserial')]
            # self.serial_port.port = filtered[0]
        elif _platform == 'win32':
            # TODO: support for Windows
            print _platform + ' currently not supported'
        else:
            print _platform + ' currently not supported'
        self.serial_port.open()

    def send(self, packet):
        self.serial_port.write(packet)
        self.serial_port.flush()

    def readline(self):
        return self.serial_port.readline()

    def receive(self):
        b = bytearray(4)
        self.serial_port.readinto(b)
        return b

    def check_for_packet(self):
        return self.serial_port.inWaiting() >= 4

    def close(self):
        self.serial_port.flushInput()
        self.serial_port.flushOutput()
        self.serial_port.close()

    def flush_buffers(self):
        self.serial_port.flushInput()
        self.serial_port.flushOutput()


def create_packet(sequence, control, pps, drums):
    packet = (sequence & 0x3) << 30
    packet |= (control & 0x3F) << 24
    packet |= (pps & 0xFF) << 16
    packet |= (drums & 0xFFFF)
    b = bytearray(4)
    for i in range(4):
        b[i] = packet >> (i*8) & 0xFF
    return b


def parse_packet(packet):
    seq = (packet[3] >> 6) & 0x3
    con = (packet[3]) & 0x3F
    pps = (packet[2] & 0x7F)
    drm = (int(packet[1]) << 8) | packet[0]
    return (seq, con, pps, drm)
