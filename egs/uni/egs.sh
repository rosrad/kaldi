#!/usr/bin/bash



export KALDI_ROOT="/work/local/renbo/kaldi/master/"
export CORPUS_ROOT="/home/renbo/work/corpus/uni_doa/"


tag="cmn_gcc"

for corpus in reverb/t60_0.3
do
    echo "training [$corpus] ..."
    ./init_dnn.py -t $tag $corpus 2>/dev/null 
    echo "evaluating ..."
    ./doa.py  "exp/data_${tag}_simu_${corpus/\//_}/"  $tag
done
