import numpy as np


def create_packet(sequence, reset, control, pps, drums):
    packet = (sequence & 0x3) << 30
    packet |= (reset & 0x1) << 29
    packet |= (control & 0xF) << 25
    packet |= (pps & 0xFF) << 16
    packet |= (drums & 0xFFFF)
    return np.uint32(packet)
