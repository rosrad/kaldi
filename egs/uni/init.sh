#!/bin/bash

# Kaldi ASR baseline for the CHiME-4 Challenge (6ch track: 6 channel track)
#
# Copyright 2016 University of Sheffield (Jon Barker, Ricard Marxer)
#                Inria (Emmanuel Vincent)
#                Mitsubishi Electric Research Labs (Shinji Watanabe)
#  Apache 2.0  (http://www.apache.org/licenses/LICENSE-2.0)

. ./path.sh
. ./cmd.sh

. utils/parse_options.sh || exit 1;

echo "$0 $@"  # Print the command line for logging
# Set bash to 'debug' mode, it will exit on :
# -e 'error', -u 'undefined variable', -o ... 'error in pipeline', -x 'print commands',
set -e
set -u
set -o pipefail

set=${1:-"no_reverb"}
tag=${2:-"entire350"}
corpus_dir=/home/renbo/work/corpus/uni_doa/simu/$set
data=data/simu/${set}/${tag}

./local/uni_simu_data_prepare.sh $corpus_dir $data
[ ! -f $data/feats.scp ] && ./steps/make_gcc.sh --nj 16 $data
./local/randsub_tr_cv.sh $data ${data}_train ${data}_eval
./local/train_doa.sh ${data}_train exp/doa/${set}_${tag}
./local/decode_doa.sh exp/doa/${set}_${tag} ${data}_eval
