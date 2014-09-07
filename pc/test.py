import sendpacket as sp
import sys


def main():
    if len(sys.argv) == 2:
        s = sp.SendPacket(sys.argv[1])
        s.send(sp.create_packet(0, 0, 0, 0, 0))
        s.send(sp.create_packet(1, 1, 1, 1, 1))
        s.send(sp.create_packet(2, 2, 2, 2, 2))
        s.send(sp.create_packet(3, 3, 3, 3, 3))
    else:
        print "Error: enter a port"


if __name__ == "__main__":
    main()
