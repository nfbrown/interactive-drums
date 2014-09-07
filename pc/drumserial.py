import serial
import numpy as np

class DrumSerial:
    serial_out = serial.Serial()

    def __init__(self, port):
        self.serial_out.baudrate = 115200
        self.serial_out.bytesize = 32
        self.serial_out.open(port)

    def send(self, packet):
        self.serial_out.write(packet)

def create_packet(sequence, reset, control, pps, drums):
    packet = (sequence & 0x3) << 30
    packet |= (reset & 0x1) << 29
    packet |= (control & 0xF) << 25
    packet |= (pps & 0xFF) << 16
    packet |= (drums & 0xFFFF)
    return np.uint32(packet)
