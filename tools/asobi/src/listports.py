#!/usr/bin/python
# listports.py -- List ALSA MIDI ports.

# Get pyalsa from here: ftp://ftp.alsa-project.org/pub/pyalsa/
from pyalsa import alsaseq

CAP_READ = alsaseq.SEQ_PORT_CAP_READ | alsaseq.SEQ_PORT_CAP_SUBS_READ
CAP_WRITE = alsaseq.SEQ_PORT_CAP_WRITE | alsaseq.SEQ_PORT_CAP_SUBS_WRITE

def is_midi_input_port(type, caps):
    return type & alsaseq.SEQ_PORT_TYPE_MIDI_GENERIC and caps & CAP_READ

def is_midi_output_port(type, caps):
    return type & alsaseq.SEQ_PORT_TYPE_MIDI_GENERIC and caps & CAP_WRITE

def get_midi_output_ports():
    input_ports, output_ports = [], []
    sequencer = alsaseq.Sequencer(name='default', clientname='listports.py',
        streams=alsaseq.SEQ_OPEN_DUPLEX, mode=alsaseq.SEQ_BLOCK)
    for connections in sequencer.connection_list():
        clientname, clientid, connectedports = connections
        for port in connectedports:
            portname, portid, connections = port
            portinfo = sequencer.get_port_info(portid, clientid)
            type, caps = portinfo['type'], portinfo['capability']
            if is_midi_input_port(type, caps):
                input_ports.append((clientid, portid, clientname, portname))
            elif is_midi_output_port(type, caps):
                output_ports.append((clientid, portid, clientname, portname))
    return input_ports, output_ports

def list_ports(ports):
    print ' Port    Client name                      Port name'
    for port in ports:
        print '%3d:%-3d  %-32.32s %s' % port

if __name__ == '__main__':
    input_ports, output_ports = get_midi_output_ports()
    print 'Input ports:'
    list_ports(input_ports)
    print '\nOutput ports:'
    list_ports(output_ports)
