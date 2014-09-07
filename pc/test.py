import drumserial as dp
import sys
import time


def main():
    if len(sys.argv) == 2:
        s = dp.DrumSerial(sys.argv[1])
        for i in range(4):
            s.send(dp.create_packet(i, i, i, i, i))
            time.sleep(0.1)
            r = dp.parse_packet(s.receive())
            if (r != (i, i, i, i, i)):
                print "Error: sent packet does not match received packet"
                break
        s.close()
    else:
        print "Error: enter a port"


if __name__ == "__main__":
    main()
