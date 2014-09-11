import drumserial as ds
import sys


def main():
    if len(sys.argv) == 2:
        n = 0
        s = ds.DrumSerial(sys.argv[1])
        for i in range(4):
            s.send(ds.create_packet(i % 4))

        while True:
            if (s.check_for_packet()):
                print ds.parse_packet(s.receive())
                s.send(ds.create_packet(n, 0, 0, 0, 0))
                n += 1
                if n > 3:
                    n = 0
    else:
        print "Error: enter a port"


if __name__ == "__main__":
    main()
