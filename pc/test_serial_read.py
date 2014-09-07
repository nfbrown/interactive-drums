import drumserial as dp
import sys


def main():
    if len(sys.argv) == 2:
        s = dp.DrumSerial(sys.argv[1])
        i = 0
        while True:
            inp = raw_input("Press Enter to send a packet or q to quit: ")
            print '', inp
            if inp is "q":
                break
            s.send(dp.create_packet(i, i % 2, i, i, i))
            print s.readline()
            i += 1
        s.close()
    else:
        print "Error: enter a port"


if __name__ == "__main__":
    main()
