#!/usr/bin/python
# connectports.py -- Connect ALSA MIDI ports.

import re
import sys

# Get pyalsa from here: ftp://ftp.alsa-project.org/pub/pyalsa/
from pyalsa import alsaseq
from pyalsa.alsaseq import *

def init_seq():
    """ opens an alsa sequencer """
    try:
        sequencer = Sequencer(name = 'default',
                              clientname = 'aconnect.py',
                              streams = SEQ_OPEN_DUPLEX,
                              mode = SEQ_BLOCK)
        return sequencer
    except SequencerError, e:
        fatal("open sequencer: %e", e)

def connect(src_port, dst_port):
    sequencer = init_seq()
    sequencer.connect_ports(src_port, dst_port)

def parse_port(string):
    m = re.match('^(\d+)(:(\d+))?$', string)
    if m:
        clientid = int(m.group(1))
        portid = m.group(3) and int(m.group(3)) or 0
        return (clientid, portid)
    raise ValueError('invalid port format')

def main():
    if len(sys.argv) < 3:
        print 'Usage: connectports.py src_port dst_port'
        exit(1)

    src_port = parse_port(sys.argv[1])
    dst_port = parse_port(sys.argv[2])
    connect(src_port, dst_port)

if __name__ == '__main__':
    main()
