# Dump a midi file.
#
# References:
# * http://www.sengpielaudio.com/calculator-notenames.htm
# * http://www.onicos.com/staff/iz/formats/midi-event.html

import sys
import midi

NoteNames = ('C', 'C#', 'D', 'D#', 'E', 'F',
             'F#', 'G', 'G#', 'A', 'A#', 'B')

def note_name(note_number):
    note = NoteNames[note_number % 12]
    octave = note_number / 12 - 1
    return '%s%s' % (note, octave)

def print_note_event(event):
    name = type(event).__name__
    tick = event.tick
    channel = event.channel
    note = event.data[0]
    velocity = event.data[1]
    print name, tick, channel, note_name(note), velocity

if len(sys.argv) != 2:
    print "Usage: {0} <midifile>".format(sys.argv[0])
    sys.exit(2)

midifile = sys.argv[1]

pattern = midi.read_midifile(midifile)
print 'format', pattern.format
print 'resolution', pattern.resolution
print 'tracks', len(pattern)
print

for i in range(len(pattern)):
    track = pattern[i]
    print 'track %d: %d events' % (i, len(track))
    print

    for event in track:
        if isinstance(event, (midi.events.NoteOnEvent,
            midi.events.NoteOffEvent)):
            print_note_event(event)
        else:
            print event
    print
