import serial
import numpy as np


class DrumSerial:
    serial_port = serial.Serial()

    def __init__(self, port):
        self.serial_port.baudrate = 115200
        self.serial_port.timeout = 5
        self.serial_port.port = port
        self.serial_port.open()

    def send(self, packet):
        self.serial_port.write(packet)

    def readline(self):
        return self.serial_port.readline()

    def receive(self):
        b = bytearray(4)
        self.serial_port.readinto(b)
        return b

    def close(self):
        self.serial_port.close()


def create_packet(sequence, reset, control, pps, drums):
    packet = (sequence & 0x3) << 30
    packet |= (reset & 0x1) << 29
    packet |= (control & 0xF) << 25
    packet |= (pps & 0xFF) << 16
    packet |= (drums & 0xFFFF)
    b = bytearray(4)
    for i in range(4):
        b[i] = packet >> (i*8) & 0xFF
    return b


def parse_packet(packet):
    seq = (packet[3] >> 6) & 0x3
    rst = (packet[3] >> 5) & 0x1
    con = (packet[3] >> 1) & 0xF
    pps = (packet[2] & 0x7F)
    drm = (int(packet[1]) << 8) | packet[0]
    return (seq, rst, con, pps, drm)
