#!/usr/bin/env python
import sys,os,shutil
import os.path as path
from optparse import OptionParser  
import subprocess

def ensure_parent(p):
    d = path.dirname(p)
    if not  path.isdir(d):
        os.makedirs(d)

def audio_list(folder, ext):
    cmd = ' '.join(['find', folder, '-type f', '-iname', '*.'+ext ])
    out =  subprocess.check_output(cmd, shell=True)
    return [ x.replace(folder,'./') for x in out.rstrip().split('\n') ]

def restruct(src,dst):
    for f in audio_list(src,'pcm'):
        nf=f.replace("_", "/")
        src_f = path.join(src,f)
        dst_f = path.join(dst,nf)
        print src_f
        ensure_parent(dst_f)
        shutil.copyfile(src_f, dst_f)
        
def test():
    src = "/home/renbo/work/corpus/uni_doa/recording/4mic_doa_record"
    restruct(src,src)

# test()

def main():
    p = OptionParser(usage="usage:%prog corpus [holder]")

    (opt,args) = p.parse_args()
    nargs= len(args)
    if nargs <1:
        p.error("no enough arguments");
        sys.exit(1)

    dst = args[0]
    if nargs >1:
        dst = args[1]

    restruct(args[0], dst)
    
if __name__ == "__main__":
    main()
