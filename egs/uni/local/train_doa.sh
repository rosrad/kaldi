#!/bin/bash


set -e # exit on error
. cmd.sh
. path.sh # source the path.
# ++++++++++++++++++++++++++++++++++++++++++++++++++
# parameters initialized
hid_layers=3
hid_dim=512
num_tgt=360
splice=5
force="no"
cmd=utils/run.pl
cmvn_opts="--norm-means"
. parse_options.sh || exit 1;

echo "$0 $@"  # Print the command line for logging
if [ $# != 2 ]; then
    echo "Usage: $0 <data-train>  <exp-dir>"
    echo " e.g.: $0 noisy-data/train  exp/doa"
    echo ""
    echo "main options (for others, see top of script file)"
    echo "  --config <config-file>   # config containing options"
    echo "  --hid-layers <N>         # number of hidden layers"
    echo "  --hid-dim <N>            # width of hidden layers"
    exit 1;
fi



data=$1
dir=$2

for f in $data/feats.scp $data/utt2doa ; do
    [ ! -f $f ] && echo "train_doa.sh: no such file $f" && exit 1;
done

if [ ! -d ${data}_tr90 ] ; then
    local/randsub_tr_cv.sh $data ${data}_tr90 ${data}_cv10 || exit 1
fi 

labels="ark:generate-post scp:${data}/feats.scp ark:${data}/utt2doa ark:- |"
# Pre-train DBN, i.e. a stack of RBMs
# --cmvn-opts "--norm-vars" \

dbn_dir=${dir}/pretrain
dbn=${dbn_dir}/${hid_layers}.dbn
if [[ ! -e "$dbn" || $force == "yes" ]]; then
    echo "pretraining RBM ..."
    $cmd $dir/log/pretrain.log \
    steps/nnet/pretrain_dbn.sh --splice ${splice} \
        --cmvn-opts ${cmvn_opts} \
        --nn-depth ${hid_layers} --hid-dim ${hid_dim} --rbm-iter 1 $data $dbn_dir 
fi

$cmd $dir/log/train.log \
    steps/nnet/train.sh --dbn ${dbn} --feature-transform "${dbn_dir}/final.feature_transform" \
    --hid-layers 0 --learn-rate 0.00001  --splice 0 \
    --labels "${labels}"  --num-tgt ${num_tgt} \
    --force "${force}" \
    ${data}_tr90 ${data}_cv10 dummy-dir dummy-dir dummy-dir $dir



