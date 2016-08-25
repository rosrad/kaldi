#!/bin/bash

# Kaldi ASR baseline for the CHiME-4 Challenge (6ch track: 6 channel track)
#
# Copyright 2016 University of Sheffield (Jon Barker, Ricard Marxer)
#                Inria (Emmanuel Vincent)
#                Mitsubishi Electric Research Labs (Shinji Watanabe)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

. ./path.sh
. ./cmd.sh

once="yes"
. utils/parse_options.sh || exit 1;

echo "$0 $@"  # Print the command line for logging
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail


corpus="/home/renbo/work/corpus/uni_doa/"

rir=${corpus}/rir/
src=${corpus}/Wakeup_words_vad/
for t60 in $(seq 0.3 0.2 1.8)
do
    rir=${corpus}/rir/t60_${t60}
    if [ ! -d $rir ] ;then
        echo "RIR wav files  of T60: ${t60} not exist! "
        continue
    fi
    dst=${corpus}/simu/reverb/t60_${t60}
    [ ! -d $dst ] && mkdir -p $dst
    opts=""
    if [[ $once == "yes" ]] ;then
        opts+=" -o "
    fi
    cmd="./local/simulate/add_rir_noise.py $opts $src $dst $rir"
    echo $cmd
    $cmd
    # ./local/simulate/add_rir_noise.py -o $src $dst $rir
done

