#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path as path
import utils
import sys
from local import compute_error
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
sets.append(["recording/20151010", "大白大白"])
sets.append(["recording/20160623_4chans", "你好魔方"])
sets.append(["recording/20160517_after_aec", "你好魔方"])  # 

def collect_er(nnet, data):
    parts = data.split('/')
    parts.insert(0,'decode')
    reg = path.join(nnet, "_".join(parts),
                    'decode.result')
    ref = path.join(data, 'utt2doa')
    er = compute_error(reg, ref)
    print "="*50
    print "Nnet : %s" % nnet
    print "data : %s" % data
    print "error: %.2f" % er
    print "="*50
    return

def oneset(s):
    data=path.join(data_dir,s[0])
    if options.er_only:
        collect_er(nnet, data)
        return

    if not  path.isfile(path.join(data, 'feats.scp')):
        opts="--mk-gcc yes"
        cmd=" ".join(["./local/data_prepare.sh",
                      opts, "--key", s[1],
                      path.join(corpus, s[0]), data])
        # print cmd
        utils.runbash(cmd)
    
    cmd=" ".join(["./local/decode_doa.sh",
                  nnet, data] )
    # print cmd
    utils.runbash(cmd)
    collect_er(nnet, data)

utils.gmap(oneset, sets, 4)
