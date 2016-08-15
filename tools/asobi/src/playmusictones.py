import sys
import time
import wave
import struct
import alsaaudio
import numpy as np

class Octave(object):
    C0 = 16.35159783128741
    HTFR = 2**(1.0/12)  # half-tone frequency ratio

    __table__ = []

    for i in range(12):
        if i == 0:
            row = [C0*(2**i) for i in range(10)]
        else:
            row = [i*HTFR for i in __table__[i-1]]
        __table__.append(row)

    __pitches__ = ['C', 'C#', 'D', 'D#', 'E', 'F',
                   'F#', 'G', 'G#', 'A', 'A#', 'B']

    @classmethod
    def tone(cls, name):
        """Get the frequency of a tone.
        e.g. tone('C4') => 440.0
        """
        if len(name) == 2:
            pitch = name[0]
        elif len(name) == 3:
            pitch = name[:2]
        else:
            raise ValueError('invalid tone name')

        if pitch not in cls.__pitches__:
            raise ValueError('invalid tone name')

        pitch = cls.__pitches__.index(pitch)

        try:
            level = int(name[-1])
        except ValueError:
            raise ValueError('invalid tone name')

        return cls.__table__[pitch][level]


def sine(freq=1000, samples=44100):
    periods = freq * samples / 44100
    return np.sin(np.linspace(0, np.pi * 2 * periods,
        samples, endpoint=False))

def quantize(real, scale=32768):
    UPPER_BOUND = scale - 1
    LOWER_BOUND = -scale

    num = int(round(real * scale))
    if num > UPPER_BOUND:
        num = UPPER_BOUND
    elif num < LOWER_BOUND:
        num = LOWER_BOUND
    return num

def pack_int16le(num):
    return struct.pack('h', num)

def sine_pcm(freq=1000, samples=44100):
    return [quantize(i) for i in sine(freq, samples)]

def sine_pcm_data(freq=1000, samples=44100):
    pcm_samples = sine_pcm(freq, samples)
    return ''.join([pack_int16le(i) for i in pcm_samples])

def tone_pcm_data(name, samples=44100):
    freq = int(round(Octave.tone(name)))
    return sine_pcm_data(freq, samples)

########################################

# prepare PCM device
device = alsaaudio.PCM(card='default')
device.setrate(44100)
device.setchannels(1)
device.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# write audio data
try:
    # C3~B6
    for i in range(3, 7):  # 3, 4, 5, 6
        for j in ['C', 'D', 'E', 'F', 'G', 'A', 'B']:
            tone = '%s%s' % (j, i)
            freq = int(round(Octave.tone(tone)))
            print tone, freq

            data = sine_pcm_data(freq)
            device.write(data)

            time.sleep(2)
except KeyboardInterrupt:
    exit()

#device.close()
