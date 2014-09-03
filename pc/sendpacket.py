import serial


class SendPacket:
    serial_out = serial.Serial()

    def __init__(self, port):
        self.serial_out.baudrate = 115200
        self.serial_out.bytesize = 32
        self.serial_out.open(port)

    def send(self, packet):
        self.serial_out.write(packet)
