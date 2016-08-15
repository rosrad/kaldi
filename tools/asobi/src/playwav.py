#!/usr/bin/env python

# This an example program in the pyalsaaudio package.

# Simple test script that plays a wav file.

# Footnote: I'd normally use print instead of sys.std(out|err).write,
# but this version runs on python 2 and python 3 without conversion

import sys
import wave
import getopt
import alsaaudio

def play(device, f):    
    nchannels = f.getnchannels()
    framerate = f.getframerate()
    sampwidth = f.getsampwidth()

    sys.stdout.write('Channels: %d\n' % nchannels)
    sys.stdout.write('Frame rate: %d\n' % framerate)
    sys.stdout.write('Sample width: %d\n' % sampwidth)

    # Set attributes
    device.setchannels(f.getnchannels())
    device.setrate(f.getframerate())

    # 8bit is unsigned in wav files
    if f.getsampwidth() == 1:
        device.setformat(alsaaudio.PCM_FORMAT_U8)
    # Otherwise we assume signed data, little endian
    elif f.getsampwidth() == 2:
        device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
    elif f.getsampwidth() == 3:
        device.setformat(alsaaudio.PCM_FORMAT_S24_LE)
    elif f.getsampwidth() == 4:
        device.setformat(alsaaudio.PCM_FORMAT_S32_LE)
    else:
        raise ValueError('Unsupported format')

    # set period size
    # Ref: http://www.alsa-project.org/main/index.php/FramesPeriods
    periodsize = framerate / 10  # interrupt every 100ms
    device.setperiodsize(periodsize)
    
    # transfer pcm data
    data = f.readframes(periodsize)
    while data:
        # Read data from stdin
        device.write(data)
        data = f.readframes(periodsize)


def usage():
    sys.stderr.write('usage: playwav.py [-c <card>] <file>\n')
    sys.exit(2)

if __name__ == '__main__':
    card = 'default'

    opts, args = getopt.getopt(sys.argv[1:], 'c:')
    for o, a in opts:
        if o == '-c':
            card = a

    if not args:
        usage()
        
    f = wave.open(args[0], 'rb')
    device = alsaaudio.PCM(card=card)

    try:
        play(device, f)
    except KeyboardInterrupt:
        pass
    finally:
        device.close()
        f.close()
