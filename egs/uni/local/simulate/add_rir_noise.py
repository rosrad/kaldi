#!/usr/bin/env python
import sys
import os
import numpy as np
from scipy.io import wavfile
from scipy.signal import fftconvolve
import os.path as path
import subprocess
from optparse import OptionParser  


def wav_list(src,ext='pcm'):
    cmd = ' '.join(['find', src, '-type f', '-iname', '*.'+ext ])
    out =  subprocess.check_output(cmd, shell=True)
    return [ x.replace(src,'./') for x in out.rstrip().split('\n') ]
    

def audio_read(f):
    [n, ext] = path.splitext(f)
    if ext.lower() == '.pcm':
        data = np.fromfile(f,dtype=np.int16)
    else:
        try:
            [fs,data] =wavfile.read(f)
        except:
            data=[]

    return data/(2.**15)
        
    
    
def mix(src_f, dst_f, ir, n, fs=16000):
    
    nchan = ir.shape[1]
    data = audio_read(src_f)
    nsample = data.shape[0]
    
    out=np.zeros((nsample,nchan))

    # import pdb; pdb.set_trace()
    
    for i in range(0,nchan):
        out[:,i]= fftconvolve(data, ir[:,i], 'same')[0:nsample]

    ensure_parent(dst_f)
    # out.tofile(dst_f)
    wavfile.write(dst_f,fs, np.int16(out*(2**15)))



def ensure_parent(p):
    d = path.dirname(p)
    if not  path.isdir(d):
        os.makedirs(d)
        

def rir_dict(dir, ics=range(0,360,5)):
    rir = {}    

    for ic in ics:
        key="degree_%d"%ic
        f = path.join(dir,key+".wav")
        [fs, h] = wavfile.read(f)
        rir[key]= 2*h/(2.**15)
    
    return rir


def mix_dir(src_dir, dst_dir, rir, once=False):
    for f in wav_list(src_dir):
        src_f = path.join(src_dir, f)
        name,ext = path.splitext(f)
        print name
        for key,ir in rir.items():
            # only support output wav format
            dst_f = path.join(dst_dir, key, name+'.wav')
            print '.',
            mix(src_f, dst_f, ir, 0)
        print 
        if once:
            break
        

def test():
    src_dir = "/home/renbo/work/corpus/uni_doa/Wakeup_words_vad/"
    dst_dir = "/home/renbo/work/test/"
    rir_dir = "/home/renbo/work/uni/local/simulate/add_noise/IR_no_T60/"
    rir = rir_dict(rir_dir)
    mix_dir(src_dir,dst_dir,rir, once=True)

# test()

def main():

    parser = OptionParser(usage="usage: %prog src_dir dst_dir rir_dir [noise_dir]",
                          version="%prog 1.0")
    parser.add_option("-o", "--once", dest="once",  
                      action="store_true", default=False,
                      help="just simulate one utterance")  

    (options, args) = parser.parse_args()  
    nargs = len(args)
    if nargs < 3:
        parser.error("no enough arguments");
        exit;


    src_dir=args[0]
    dst_dir=args[1]
    rir_dir=args[2]
    
    if nargs == 4:
        noise_dir=args[3]
        

    rir = rir_dict(rir_dir)
    mix_dir(src_dir,dst_dir,rir, options.once)
    
if __name__ == '__main__':
    main()

