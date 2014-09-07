import drumserial as dp
import sys


def main():
    if len(sys.argv) == 2:
        s = dp.DrumSerial(sys.argv[1])
        for i in range(0, 4):
            s.send(dp.create_packet(i, i % 2, i, i, i))
            print "Sent packet: (%d, %d, %d, %d, %d)" % (i, i % 2, i, i, i)
            r = dp.parse_packet(s.receive())
            print "Received packet: ", r
            if (r != (i, i % 2, i, i, i)):
                print "Error: sent packet does not match received packet"
                break
        s.close()
    else:
        print "Error: enter a port"


if __name__ == "__main__":
    main()
