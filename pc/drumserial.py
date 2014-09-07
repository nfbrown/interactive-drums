import serial
import numpy as np

class DrumSerial:
    serial_port = serial.Serial()

    def __init__(self, port):
        self.serial_port.baudrate = 115200
        self.serial_port.bytesize = 32
        self.serial_port.open(port)

    def send(self, packet):
        self.serial_port.write(packet)

    def receive(self):
        self.serial_port.read(4)

    def close(self):
        self.serial_port.close()

def create_packet(sequence, reset, control, pps, drums):
    packet = (sequence & 0x3) << 30
    packet |= (reset & 0x1) << 29
    packet |= (control & 0xF) << 25
    packet |= (pps & 0xFF) << 16
    packet |= (drums & 0xFFFF)
    return np.uint32(packet)


def parse_packet(packet):
    seq = (packet >> 30) & 0x3
    rst = (packet >> 29) & 0x1
    con = (packet >> 25) & 0xF
    pps = (packet >> 16) & 0xFF
    drm = (packet & 0xFFFF)
    return (seq, rst, con, pps, drm)
