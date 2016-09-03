#!/usr/bin/env python
import sys,os,shutil
import os.path as path
import subprocess

def pcm_pipeline(pcm, fs=16000,chan=4, byte=16):
    tool = path.join(os.environ["KALDI_ROOT"],"tools/pcm2wav/pcm2wav")
    return [tool, pcm, "- %d %d %d |"% (chan, fs, byte) ]
def work_root():
    return path.join(os.environ['KALDI_ROOT'], "egs/uni/")

def corpus_root():
    if "CORPUS_ROOT" in os.environ:
        return os.environ["CORPUS_ROOT"]
    else:
        return "/home/renbo/work/corpus/uni_doa/"


def decode_path(nnet, data):
    parts = data.split('/')
    parts.insert(0,'decode')
    return path.join(nnet, "_".join(parts))

    
def read_table(f):
    d = {}
    with open(f, 'rb') as inf:
        for line in inf:
            parts = line.split()
            d[parts[0]] = parts[1:]
            
    return d
    
def write_table(f,d):
    if not d:
        return
    if isinstance(d, (list,tuple)):  # convert list into dict
        d = {x:[] for x in d }

    with open(f, 'wb') as wf:
        for k in sorted(d):
            v = [ str(i) for i in d[k]]
            wf.write("%s %s\n"%(k, " ".join(v)))
    
def ensure_dir(d):
    if not  path.isdir(d):
        os.makedirs(d)

def audio_list(folder, ext):
    cmd = ' '.join(['find', folder, '-type f', '-iname', '*.'+ext ])
    out =  subprocess.check_output(cmd, shell=True)
    return [ path.relpath(x.replace(folder,'./')) for x in out.rstrip().split('\n') if x ]

def revert_table(d):
    rd = {} 
    for k,v in d.iteritems():
        if v[0] in rd.keys():
            rd[v[0]] = rd[v[0]]+[k]
        else:
            rd[v[0]] = [k]
    return rd
    
def mk_feat(data):
    # make features
    cmd = " ".join( [work_root()+"./steps/make_gcc.sh --nj 16",data])
    subprocess.call(cmd, shell=True)

    # make cmvn
    cmd = " ".join( [work_root()+"./steps/compute_cmvn_stats.sh", data])
    subprocess.call(cmd, shell=True)
    


