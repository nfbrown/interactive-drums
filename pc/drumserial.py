import serial


class DrumSerial:
    serial_port = serial.Serial()

    def __init__(self, port):
        self.serial_port.baudrate = 115200
        self.serial_port.timeout = 5
        self.serial_port.port = port
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
    packet |= (control & 0x1F) << 25
    packet |= (pps & 0xFF) << 16
    packet |= (drums & 0xFFFF)
    b = bytearray(4)
    for i in range(4):
        b[i] = packet >> (i*8) & 0xFF
    return b


def parse_packet(packet):
    seq = (packet[3] >> 6) & 0x3
    con = (packet[3] >> 1) & 0x1F
    pps = (packet[2] & 0x7F)
    drm = (int(packet[1]) << 8) | packet[0]
    return (seq, con, pps, drm)
