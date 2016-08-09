#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path as path
import utils

set="doa_360_degree_data_no_reverb"
nnet=path.join("exp/doa/", set)

corpus="/home/renbo/work/corpus/uni_doa/"
sets=[]
sets.append(["recording/20151010", "大白大白"])
sets.append(["recording/20160623_4chans", "你好魔方"])
# sets.append(["recording/20160517_after_aec", "你好魔方"])

def oneset(s):
    data=path.join("data",s[0])
    if not  path.isfile(path.join(data, 'feats.scp')):
        cmd=" ".join(["./local/data_prepare.sh",
                  "--key", s[1], path.join(corpus, s[0]), data])
        # print cmd
        utils.runbash(cmd)
    
    cmd=" ".join(["./local/decode_doa.sh",
                  nnet, data] )
    # print cmd
    utils.runbash(cmd)

utils.gmap(oneset, sets, 4)
