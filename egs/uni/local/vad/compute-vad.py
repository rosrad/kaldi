#!/usr/bin/env python
import sys
import inspect
import os.path as path
from optparse import OptionParser  
import subprocess

def audio_list(folder, ext):
    cmd = ' '.join(['find', folder, '-type f', '-iname', '*.'+ext ])
    out =  subprocess.check_output(cmd, shell=True)
    return [ x.replace(folder,'./') for x in out.rstrip().split('\n') ]

def walk_dir(src,dst,nchan,ext):

    for f in audio_list(src,ext):
        src_f = path.join(src, f)
        name,ext = path.splitext(f)
        dst_f = path.join(dst, name+'.txt')
        print src_f
        vad(src_f,dst_f,nchan)


    
def vad(src,dst, nchan):
    cur_py=inspect.getfile(inspect.currentframe())
    exe_dir=path.dirname(cur_py)
    exe = path.join(exe_dir, "vad_lab_%dch.exe"%nchan)
    cmd = " ".join([exe, src, dst])
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE
                     ,stderr=subprocess.PIPE)
    out, err = p.communicate()
    # print(out)

def test():
    src_dir = "/home/renbo/work/corpus/uni_doa/Wakeup_words/"
    walk_dir(src_dir, src_dir, 1, "pcm")

# test()

def main():
    parser = OptionParser()  
    parser.add_option("-c", "--chan", dest="chan",
                      action="store", type="int",
                      help="number of channels", default=4)
    parser.add_option("-e", "--ext", dest="ext",
                      action="store", help="ext of audio files",
                      default="pcm")
    
    
    (options, args) = parser.parse_args()  
    narg = len(args)
    if narg < 1:
        parser.error("No enough parameters")
        sys.exit()
    src = args[0];
    dst = args[0];
    if narg > 1:
        dst = args[1]

    if path.isdir(src):
        walk_dir(src,dst, options.chan, options.ext)
    else:
        if dst == src:
            [p, ext] = path.splitext(src)
            dst = path.join(p, '.txt')

        vad(src,dst, options.chan)

if __name__ == '__main__':
    main()
