#!/usr/bin/env python

import sys
import wave

def wavinfo(filename):
    wf = wave.open(filename, 'rb')

    nchannels = wf.getnchannels()
    sampwidth = wf.getsampwidth() * 8  # bits
    framerate = wf.getframerate()
    nframes = wf.getnframes()
    duration = 1.0 * nframes / framerate

    wf.close()

    return '%d chan, %d bit, %d Hz, %d frames, %.0f seconds' % \
        (nchannels, sampwidth, framerate, nframes, duration)

def main():
    for arg in sys.argv[1:]:
        try:
            print '%s: %s' % (arg, wavinfo(arg))
        except Exception, e:
            print '%s: %s' % (arg, e)

if __name__ == '__main__':
    main()
