#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path as path
import utils
import sys
from local import collect_error
from local import build_all
from optparse import OptionParser  

parser = OptionParser()
parser.add_option("-e", "--er-only",  
                  action="store_true", dest="er_only", default=False,  
                  help="compute the error rate only")  

(options, args) = parser.parse_args()

narg=len(args);
if narg < 1:
    print "No enough parameters"
    print "doa.py nnet_dir [data/350]"
    sys.exit()

nnet = args[0];
data_dir = "data"
if narg>=2:
    data_dir = args[1]

# set="no_reverb"
# nnet=path.join("exp/doa/", set)

corpus="/home/renbo/work/corpus/uni_doa/"
sets=[]
sets.append(["recording/20151010", "大白大白", "pcm"])
sets.append(["recording/20160623_4chans", "你好魔方", "pcm"])
sets.append(["recording/20160517_after_aec", "你好魔方", "pcm"])  # 
sets.append(["recording/2016_4mic", "","pcm"])  # 
def write_list(f, l):
    with open(f, 'wb') as wf:
        for i in l:
            wf.write(i+'\n')

def decode_dir(nnet, data):
    parts = data.split('/')
    parts.insert(0,'decode')
    return path.join(nnet, "_".join(parts))

def analysis_err(nnet,data):
    dir=decode_dir(nnet,data)

    cmd=" ".join(['./local/err_egs.sh', dir, data])
    utils.runbash(cmd)
    
def collect_er(nnet, data):
    dir=decode_dir(nnet,data)
    reg = path.join(dir, 'decode.result')
    err_keys = path.join(dir, "err.keys")
    ref = path.join(data, 'utt2doa')
    (er,errors) = collect_error(reg, ref)
    write_list(err_keys, errors)
    print "="*50
    print "decoded : %s" % reg
    print "ref : %s" % ref
    print "error: %.2f" % er
    print "="*50

def oneset(s):
    data=path.join(data_dir,s[0])
    if options.er_only:
        collect_er(nnet, data)
        return

    if not  path.isfile(path.join(data, 'feats.scp')):
        build_all(path.join(corpus, s[0]), data,
                  ext=s[2], filter=s[1])
        
    cmd=" ".join(["./local/decode_doa.sh",
                  nnet, data] )
    # print cmd
    utils.runbash(cmd)
    collect_er(nnet, data)
    analysis_err(nnet,data)

utils.gmap(oneset, sets, 4)
