#!/usr/bin/bash



export KALDI_ROOT="/work/local/renbo/kaldi/master/"
export CORPUS_ROOT="/home/renbo/work/corpus/uni_doa/"


tag="raw-gcc"

for corpus in clean.RIR0.13.vad reverb/t60_0.3
do
    echo "training [$corpus] ..."
    ./init_dnn.py -t $tag $corpus 2>/dev/null 

    echo "evaluating ..."
    ./doa.py  "exp/data_${tag/-/_}_simu_${corpus/-/_}/"  $tag
done
