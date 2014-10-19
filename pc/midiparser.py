import mido
import drumserial as ds

supported_drums = [36, 38, 47, 48]


def midi_to_packets(filename):
    mf = mido.MidiFile(filename)
    beats_per_second = 1000000.0 / 500000
    tempo_list = [i for i in mf
                  if type(i) == mido.MetaMessage and i.type == 'tempo']
    if tempo_list != []:
        beats_per_second = 1000000.0 / tempo_list[0].tempo

    packets_per_second = beats_per_second * 4.0
    note_ons = [i for i in mf if type(i) == mido.Message
                and i.type == 'note_on']
    m = [(i.note, i.velocity, i.time) for i in note_ons]
    return tuples_to_packets(delta_time_to_seconds(m, packets_per_second),
                             packets_per_second)


def delta_time_to_seconds(note_on_tuples, pps):
    total = 0
    new_tuples = []
    print note_on_tuples
    for i in note_on_tuples:
        delta_packets = (round_to(i[2], 1.0 / pps) * pps)
        total += delta_packets
        print delta_packets
        new_tuples.append((i[0], i[1],
                           total * pps, int(delta_packets)))

    return [i for i in new_tuples if i[1] != 0]


def tuples_to_packets(note_on_tuples, pps):
    packets = []
    i = 0
    seq = 0
    period = (1.0/pps)*(32000)
    packets.append(ds.create_packet(0, 0, int(period) >> 5, 0))
    while (i < len(note_on_tuples)):
        filtered = [x for x in note_on_tuples if x[2] == note_on_tuples[i][2]]
        drums = 0
        for x in range(note_on_tuples[i][3]):
            packets.append(ds.create_packet(seq % 4, 0, 0, drums))
            seq += 1
        for x in filtered:
            try:
                drum_index = supported_drums.index(x[0])
                drums |= 0x1 << drum_index
            except ValueError:
                print str(x[0]) + ' is not in the list of supported MIDI drums.'
        packets.append(ds.create_packet(seq % 4, 0, 0, drums))
        seq += 1
        i += len(filtered)
    return packets


def round_to(n, precision):
    return round(n / precision) * precision
