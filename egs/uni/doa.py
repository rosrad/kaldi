#!/usr/bin/env python
# -*- coding: utf-8 -*-  
import os.path as path
import utils
import sys
from local import *
from optparse import OptionParser  


def write_list(f, l):
    with open(f, 'wb') as wf:
        for i in l:
            wf.write(i+'\n')


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
    mk_err(egs,data)

class Evaluator(object):
    """ 
    evaluate a data set for dnn
    """
    setname=""
    tag=""
    data=""
    audio_dir=""
    audio_ext="wav"
    label_filter=""
    wrk_dir=""
    er=0.0
    def __init__(self, setname,tag, ext="wav", filter=""):
        self.setname = setname
        self.tag=tag
        self.data = path.join("data",self.tag,self.setname)

        self.audio_dir = path.join(corpus_root(),
                                   self.setname)
        self.audio_ext = ext
        self.label_filter = filter

        # if not exist, build it;
        if not  path.isfile(path.join(self.data, 'feats.scp')):
            build_all(self.audio_dir, self.data,
                      self.audio_ext, self.label_filter)

    def _decode_dnn(self,nnet):
        cmd=" ".join(["./local/decode_doa.sh",
                  nnet, self.data] )
        # print cmd
        utils.runbash(cmd)

    def decode_eval(self,nnet):
        self._decode_dnn(nnet)
        self.eval(nnet, True)
        
    def eval(self,nnet, mk_egs=True):
        self.wrk_dir=decode_path(nnet,self.data)
        reg = path.join(self.wrk_dir, 'decode.result')
        ref = path.join(self.data, 'utt2doa')
        self.er, self.errors = collect_error(reg, ref)

        # write error utterance keys
        key_f = path.join(self.wrk_dir, "err.keys")
        write_table(key_f, self.errors)

        if mk_egs:
            cmd=" ".join(['./local/err_egs.sh', self.wrk_dir, self.data])
            utils.runbash(cmd)

    def __repr__(self):
        return "\n".join(
            [ "="*50,
              "decoded : %s" % self.wrk_dir,
              "error: %.2f" % self.er,
              "="*50])



def evaluate_all(nnet,tag, eval_only=True):
    sets=[]
    # sets.append(["相对目录", "过滤单词", "后缀格式"])
    sets.append(["recording/20151010", "大白大白", "pcm"])
    sets.append(["recording/20160623_4chans", "你好魔方", "pcm"])
    sets.append(["recording/20160517_after_aec", "你好魔方", "pcm"])  # 
    sets.append(["recording/4mic_2016", "","pcm"])  #
    sets.append(["recording/20160810_aec_4chans", "你好魔方","out"])  #
    for s in sets:
        ev = Evaluator(s[0],tag, s[2], s[1] )
        if eval_only:
            ev.eval(nnet,mk_egs=False)
        else:
            ev.decode_eval(nnet)
        print ev
        # utils.gmap(oneset, sets, 4)

def main():
    p = OptionParser(usage="usage: %prog exp tag")
    p.add_option("-e", "--eval-only",  
                  action="store_true", dest="eval_only", default=False,  
                  help="no decode step")  

    (opt, args) = p.parse_args()
    narg=len(args);
    if narg < 2:
        p.error("No enough parameters")
        sys.exit(1)

    evaluate_all(args[0], args[1], opt.eval_only)
    

if __name__ == "__main__":
    main()
