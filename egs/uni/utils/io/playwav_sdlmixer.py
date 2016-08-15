# Play a wave file with SDL mixer.
# It is not suitable for playing long music.
# physacco 2013

import sys
import wave
import numpy
import struct
import pygame
from pygame.locals import *

def play_wave(wavef, channel, sample_rate):
    data = wavef.readframes(sample_rate)
    if not len(data):
        return False

    play_frames(channel, data)
    return True

def play_frames(channel, data):
    nframes = len(data) / 4
    buf = numpy.zeros((nframes, 2), dtype = numpy.int16)
    for i in range(nframes):
        buf[i][0], buf[i][1] = struct.unpack('hh', data[i*4:(i+1)*4])

    sound = pygame.sndarray.make_sound(buf)
    channel.play(sound)

def main():
    # open wave file
    path = sys.argv[1]
    wavef = wave.open(path, 'rb')

    nchannels = wavef.getnchannels()
    sampwidth = wavef.getsampwidth()
    framerate = wavef.getframerate()
    print '%d channels, %d bits, %d Hz' % (nchannels, sampwidth, framerate)

    # init pygame
    pygame.mixer.pre_init(framerate, -sampwidth*8, nchannels)
    pygame.init()
    pygame.display.set_mode((640, 480))

    channel = pygame.mixer.find_channel()
    channel.set_endevent(pygame.USEREVENT)

    # play wave file
    play_wave(wavef, channel, framerate)

    # main loop
    _running = True
    while _running:
        for event in pygame.event.get():
            print event
            if event.type == pygame.QUIT:
                _running = False
                break
            elif event.type == pygame.USEREVENT:
                # big latency!
                cont = play_wave(wavef, channel, framerate)
                if not cont:
                    print 'playback finished'
                    _running = False
                    break

    # shutdown
    pygame.quit()

if __name__ == '__main__':
    main()
