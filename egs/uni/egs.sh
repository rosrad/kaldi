#!/usr/bin/bash



export KALDI_ROOT="/work/local/renbo/kaldi/master/"
export CORPUS_ROOT="/home/renbo/work/corpus/uni_doa/"

echo "training step ..."
./init_dnn.py -t "raw-gcc" "reverb/t60_0.3" 2>/dev/null 

echo "evaluating step ..."
./doa.py -t "raw-gcc" "exp/data_raw_gcc_simu_reverb_t60_0.3/"
