import sys
import wave
import struct
import alsaaudio
import numpy as np

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

########################################

if len(sys.argv) >= 2:
    F = int(sys.argv[1])
else:
    F = 1000     # 1000 Hz

# generate audio data
data = sine_pcm_data(F, 4410)

# prepare PCM device
device = alsaaudio.PCM(card='default')
device.setrate(44100)
device.setchannels(1)
device.setformat(alsaaudio.PCM_FORMAT_S16_LE)
device.setperiodsize(44100)

# write audio data
try:
    while True:
        device.write(data)
except KeyboardInterrupt:
    exit()

#device.close()
