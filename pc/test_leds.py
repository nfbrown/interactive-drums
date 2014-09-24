import drumserial as ds
import sys

leds = [7, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0]  # Simple drum pattern


def main():
    if len(sys.argv) == 2:
        n = 13
        s = ds.DrumSerial(sys.argv[1])
        for i in range(13):
            s.send(ds.create_packet(i % 4, 0, 0, 0, leds[i]))

        while True:
            if (s.check_for_packet()):
                print ds.parse_packet(s.receive())
                s.send(ds.create_packet(n % 4, 0, 0, 0, leds[n]))
                n += 1
                if n > 15:
                    n = 0
    else:
        print "Error: enter a port"


if __name__ == "__main__":
    main()
