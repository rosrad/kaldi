#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path as path

import sys
from local import build_all
from local import runbash
from local import corpus_root
from optparse import OptionParser  

def build_data(name, tag):
    audio_dir = path.join(corpus_root(), "simu",name)
    data_dir = path.join("data",tag, "simu",name)
    if not path.isfile(path.join(data_dir, "feats.scp")):        
        build_all(audio_dir, data_dir, ext="wav")
    return data_dir

def run_dnn(data, force=False):
    tr = data+"train"
    ev = data+"eval"
    # sub training data
    cmd = " ".join(["./local/randsub_tr_cv.sh",
                   data,tr,ev])
    runbash(cmd)

    dnn = path.join("exp",data.replace("/","_"))
    # train dnn
    opts=""
    if force:
        opts = "--force yes"

    cmd = " ".join(["./local/train_doa.sh",
                    opts, tr, dnn])

    print cmd
    runbash(cmd)
    # decode dnn
    cmd = " ".join(["./local/decode_doa.sh",
                    dnn, ev])
    print cmd
    runbash(cmd)
    
def test():
    name = "reverb/t60_1.8"
    tag = "raw_gcc"
    data = build_data(name,tag)
    print data
    run_dnn(data)
# test()
                    
def main():
    p = OptionParser(usage="usage: %prog set ")
    p.add_option( "-t","--tag", dest="tag",  
                      action="store", default="gcc",
                      help="tag name")  

    p.add_option( "-f","--force", dest="force",  
                  action="store_true", default=False,
                  help="force retrain dnn")  

    (opt, args) = p.parse_args()
    narg=len(args);
    if narg <1:
        p.error("no enough arguments!")
        sys.exit()

    data = build_data(args[0], opt.tag)
    print "run dnn on : [%s]"%data
    run_dnn(data, opt.force)


if __name__ == "__main__":
    main()
