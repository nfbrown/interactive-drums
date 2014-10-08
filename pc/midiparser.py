import mido
# import re


def midi_to_packets(filename):
    messages = [i for i in mido.MidiFile(filename) if type(i) == mido.Message
                and i.type == 'note_on'
                and i.velocity != 0]
    m = [(i.note, i.time) for i in messages]
    print m


def main():
    midi_to_packets("example.mid")


if __name__ == "__main__":
    main()
