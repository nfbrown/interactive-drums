import mido
# import re


def midi_to_packets(filename):
    mf = mido.MidiFile(filename)
    ticks_per_beat = mf.ticks_per_beat
    seconds_per_beat = 0.5
    tempo_list = [i for i in mf
                  if type(i) == mido.MetaMessage and i.type == 'tempo']
    if tempo_list != []:
        seconds_per_beat = tempo_list[0].tempo / 1000000.0

    seconds_per_tick = seconds_per_beat / ticks_per_beat
    note_ons = [i for i in mf if type(i) == mido.Message
                and i.type == 'note_on']
    meta_messages = [i for i in mf
                     if type(i) == mido.MetaMessage]
    m = [(i.note, i.velocity, float(i.time)) for i in note_ons]
    print delta_time_to_seconds(m, seconds_per_tick)


def delta_time_to_seconds(note_on_tuples, seconds_per_tick):
    total = float(0.0)
    new_tuples = []
    for i in note_on_tuples:
        total += i[2]
        new_tuples.append((i[0], i[1], total))
    return [i for i in new_tuples if i[1] != 0]


def main():
    midi_to_packets("example.mid")


if __name__ == "__main__":
    main()
