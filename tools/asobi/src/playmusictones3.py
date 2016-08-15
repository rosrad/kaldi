import re
import sys
import wave
import struct
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

def translate_numnote(name, base=4):
    alpha = 'CDEFGAB'

    m = re.match("^(\d)(,*|'*)([\*\/]\d+)?$", name)
    if not m:
        raise ValueError("invalid notation '%s'" % name)

    a, b, c = m.groups()

    tone = alpha[int(a)-1]

    if not b:
        level = base
    elif b[0] == "'":
        level = base + len(b)
    else:
        level = base - len(b)

    if not c:
        length = 1
    elif c[0] == '*':
        length = 1 * int(c[1:])
    else:
        length = 1.0 / int(c[1:])

    tone = '%s%s' % (tone, level)

    return (tone, length)

def numnote_pcm_data(name, base=4, samples=44100):
    tone, length = translate_numnote(name, base)
    return tone_pcm_data(tone, int(samples * length))

def save_music(wf, seq, base=4, beatlen=1):
    beats = 0
    for i in seq:
        tone, length = translate_numnote(i, base)
        samples = int(44100 * beatlen * length)
        data = tone_pcm_data(tone, samples)
        wf.writeframes(data)
        beats += length

    playtime = beats * beatlen  # seconds
    print 'beats: %s, playtime: %s' % (beats, playtime)

########################################

score = """
1''/2  7'/2  1''/2  3''/2  7'*2
6'/2  5'/2  6'/2  1''/2  5'*2
4'/2  3'/2  4'/2  1''/2  7'  5'
6'/2  7'/2  1''/2  3''/2  2''*2
1''/2  7'/2  1''/2  3''/2  7'  5'
6'/2  7'/2  1''/2  2''/2  3''  3''
4''/2  3''/2  2''/2  1''/2  7'/2  3''/2  5'/2  7'/2
6'*4
"""

score = re.split('\s+', score.strip())

wf = wave.open('hoshi_no_arika.wav', 'wb')
wf.setnchannels(1)
wf.setframerate(44100)
wf.setsampwidth(2)

save_music(wf, score, base=4, beatlen=0.5)

wf.close()
