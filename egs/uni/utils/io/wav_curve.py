# Draw the amplitute of a wave file.
# Requires numpy and matplotlib.

import sys
import wave
import struct
import matplotlib
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import matplotlib.animation as animation

wf = wave.open(sys.argv[1], 'rb')

nchannels = wf.getnchannels()
framerate = wf.getframerate()
sampwidth = wf.getsampwidth()
sys.stdout.write('Channels: %d\n' % nchannels)
sys.stdout.write('Frame rate: %d\n' % framerate)
sys.stdout.write('Sample width: %d\n' % sampwidth)

class Scope:
    def __init__(self, ax, maxt=1000, dt=1):
        self.ax = ax
        self.dt = dt
        self.maxt = maxt
        self.tdata = [0]
        self.ydata = [0]
        self.line = Line2D(self.tdata, self.ydata)
        self.ax.add_line(self.line)
        #self.ax.set_ylim(-32768, 32767)
        self.ax.set_ylim(-5000, 5000)
        self.ax.set_xlim(0, self.maxt)

    def update(self, y):
        lastt = self.tdata[-1]
        if lastt > self.tdata[0] + self.maxt: # reset the arrays
            self.tdata = [self.tdata[-1]]
            self.ydata = [self.ydata[-1]]
            self.ax.set_xlim(self.tdata[0], self.tdata[0] + self.maxt)
            self.ax.figure.canvas.draw()

        t = self.tdata[-1] + self.dt
        self.tdata.append(t)
        self.ydata.append(y)
        self.line.set_data(self.tdata, self.ydata)
        return self.line,


def emitter():
    count = 0
    while True:
        data = wf.readframes(framerate*interval)
        if not len(data):
            break

        framesize = nchannels * sampwidth
        nframes = len(data) / framesize
        print nframes
        count += nframes
        if count % 100 == 0:
            print count
        sum = 0
        for i in range(0, len(data), framesize):
            if nchannels == 1:
                l = struct.unpack('h', data[i:i+framesize])[0]
                sum += l
            elif nchannels == 2:
                l, r = struct.unpack('hh', data[i:i+framesize])
                sum += l
            else:
                raise 'invalid nchannels: %s' % nchannels
        avg = 1.0 * sum / nframes
        yield avg


interval = 0.01  # 0.01 sec
xmax = 10  # x-axis: 10 sec

fig = plt.figure()
ax = fig.add_subplot(111)
scope = Scope(ax, maxt=xmax, dt=interval)

ani = animation.FuncAnimation(fig, scope.update, emitter,
    interval=interval*1000, blit=True)

plt.show()
