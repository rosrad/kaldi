#!/usr/bin/env python

import sys
import wave

def transfer(wf, outf, nchannels, framerate, sampwidth):    
    framesize = nchannels * sampwidth

    nframes = 0
    while True:
        data = wf.readframes(framerate)
        if not len(data):
            break
        outf.write(data)
        nframes += len(data) / framesize

    return nframes

def convert(input, output):
    wf = wave.open(input, 'rb')

    nchannels = wf.getnchannels()
    framerate = wf.getframerate()
    sampwidth = wf.getsampwidth()

    sys.stdout.write('Channels: %d\n' % nchannels)
    sys.stdout.write('Frame rate: %d\n' % framerate)
    sys.stdout.write('Sample width: %d\n' % sampwidth)

    with open(output, 'w') as outf:
        nframes = transfer(wf, outf, nchannels, framerate, sampwidth)
        print 'nframes: %s' % nframes
        print 'nbytes: %s' % (nframes * nchannels * sampwidth)
    wf.close()

def usage():
    print 'wav2pcm INPUT OUTPUT'

def version():
    print 'wav2pcm 0.1.0'

def main():
    if len(sys.argv) < 3:
        usage()
        exit(1)

    convert(sys.argv[1], sys.argv[2])

if __name__ == '__main__':
    main()
