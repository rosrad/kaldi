#!/usr/bin/env python
import sys,os,shutil
import os.path as path
from optparse import OptionParser  
# import numpy as np
import re
import subprocess



def pcm_pipeline(pcm, fs=16000,chan=4, byte=16):
    tool = "/work/local/renbo/kaldi/master//tools/pcm2wav/pcm2wav"
    return [tool, pcm, "- %d %d %d |"% (chan, fs, byte) ]
def work_root():
    return path.join(os.environ['KALDI_ROOT'], "egs/uni/")

def read_table(f):
    d = {}
    with open(f, 'rb') as inf:
        for line in inf:
            parts = line.split()
            d[parts[0]] = parts[1:]
            
    return d
    
def write_table(f,d):
    with open(f, 'wb') as wf:
        for k in sorted(d):
            v = d[k]
            wf.write("%s %s\n"%(k, " ".join(v)))
    
def ensure_dir(d):
    if not  path.isdir(d):
        os.makedirs(d)

def audio_list(folder, ext):
    cmd = ' '.join(['find', folder, '-type f', '-iname', '*.'+ext ])
    out =  subprocess.check_output(cmd, shell=True)
    return [ path.relpath(x.replace(folder,'./')) for x in out.rstrip().split('\n') if x ]

def build_data(src, data, ext="wav",filter=""):
    ensure_dir(data)
    # with open(wav_scp, 'w') as wf:
    wav_dict = {}
    segment_dict = {}
    for f in audio_list(src,ext):
        name,ext = path.splitext(f)
        key = name.replace("/","_")
        print key
        if ext.lower() == '.wav':
            wav_dict[key]=[path.join(src, f)]
        else:
            wav_dict[key] = pcm_pipeline(path.join(src, f))
            # we need the segment lable
            label = path.join(src, name+".txt")
            segment_dict.update(segment(key, label,filter))

    keys = wav_dict.keys()
    if segment_dict:
        keys = segment_dict.keys()

        
    write_table(path.join(data,"wav.scp"), wav_dict)
    write_table(path.join(data,"segments"), segment_dict)
    doa_dict = key2doa(keys)
    
    write_table(path.join(data,"utt2doa"), doa_dict)
    write_table(path.join(data,"utt2spk"), doa_dict)    
    spk2utt = revert_table(doa_dict)
    write_table(path.join(data,"spk2utt"), spk2utt)    

def key2doa(keys, fixed=-1):
    com = re.compile(r'((\d+)c)|(degree_(\d+))')
    d = {}
    for k in keys:
        doas = [ s for s in com.search(k).groups() if s and s.isdigit() ] 
        if doas:
            d[k] = [doas[0]]
        else:
            d[k] = [-1]

    return d

def revert_table(d):
    rd = {} 
    for k,v in d.iteritems():
        if v[0] in rd.keys():
            rd[v[0]] = rd[v[0]]+[k]
        else:
            rd[v[0]] = [k]
    return rd
    
def segment(k, f, filter=""):
    if not path.isfile(f):
        return {}
    d = {}
    with open(f, 'rb') as inf:
        for line in inf:
            if line.find(filter) <0:
                continue
            
            parts = line.split()
            if len(parts) < 2:
                continue
            
            key = "_".join([k,parts[0]])
            d[key] = [k]+parts[0:2]

    return d
    
def mk_feat(data):
    # make features
    cmd = " ".join( [work_root()+"./steps/make_gcc.sh --nj 16",data])
    subprocess.call(cmd, shell=True)

    # make cmvn
    cmd = " ".join( [work_root()+"./steps/compute_cmvn_stats.sh", data])
    subprocess.call(cmd, shell=True)
    
def build_all(src, data, ext="wav", filter=""):
    build_data(src,data, ext,filter)

    if path.isfile(path.join(data,"wav.scp")):
        print "make features : [%s]"%data
        mk_feat(data)

        
    
def test():
    src = "/home/renbo/work/corpus/uni_doa/recording/2016_4mic_wavs"
    data = "/home/renbo/work/uni/data/raw_gcc/recording/2016_4mic_wavs" 
    src = "/home/renbo/work/corpus/uni_doa/recording/2016_4mic"
    data = "/home/renbo/work/uni/data/raw_gcc/recording/2016_4mic" 

    build_all(src,data, ext='pcm')

# test()

def main():
    p = OptionParser(usage="usage:%prog corpus data")
    p.add_option( "-e","--ext", dest="ext",  
                      action="store", default="wav",
                      help="corpus audio file extention")  
    (opt,args) = p.parse_args()
    nargs= len(args)
    if nargs <2:
        p.error("no enough arguments");
        sys.exit(1)

    build_all(args[0], args[1], opt.ext)
    
if __name__ == "__main__":
    main()
