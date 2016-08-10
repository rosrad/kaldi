#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path as path
import utils
import sys

narg=len(sys.argv);
if narg < 2:
    print "No enough parameters"
    print "doa.py nnet_dir [data/350]"
    sys.exit()

nnet = sys.argv[1];
data_dir = "data"
if narg>=3:
    data_dir = sys.argv[2]

# set="no_reverb"
# nnet=path.join("exp/doa/", set)

corpus="/home/renbo/work/corpus/uni_doa/"
sets=[]
sets.append(["recording/20151010", "大白大白"])
sets.append(["recording/20160623_4chans", "你好魔方"])
sets.append(["recording/20160517_after_aec", "你好魔方"])  # 

def oneset(s):
    data=path.join(data_dir,s[0])
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

utils.gmap(oneset, sets, 4)
