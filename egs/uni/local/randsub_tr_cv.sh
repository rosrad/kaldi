#!/bin/bash
cv_utt_percent=10 # default 10% of total utterances 
seed=777 # use seed for speaker shuffling
# End configuration.
echo "$0 $@"  # Print the command line for logging
uttbase=true; # by default, we choose last 10% utterances for CV
. parse_options.sh || exit 1;

if [ $# != 3 ]; then
    echo "Usage: $0 [options] <srcdir> <traindir> <crossvaldir>"
    echo "Options:"
    echo "  --cv-utt-percent P  Cross Validation portion of the total utterances, default is 10% (i.e. P=10)"
    echo "  "
    exit 1;
fi

srcdir=$1
trndir=$2
cvdir=$3

[ ! -d $trndir ] && mkdir -p $trndir
[ ! -d $cvdir ] && mkdir -p $cvdir
#total number of lines
N=$(cat $srcdir/utt2spk | wc -l)
#get line number where (100-P)% of the data lies
N_cv=$((N * cv_utt_percent / 100))
N_tr=$((N - N_cv))
awk '{print $1}' $srcdir/utt2spk | utils/shuffle_list.pl --srand $seed > $trndir/_tmpf_randutt
head -n $N_cv $trndir/_tmpf_randutt > $cvdir/_tmpf_cv
tail -n $N_tr $trndir/_tmpf_randutt > $trndir/_tmpf_tr
utils/subset_data_dir.sh --utt-list $trndir/_tmpf_tr $srcdir $trndir
utils/subset_data_dir.sh --utt-list $cvdir/_tmpf_cv  $srcdir $cvdir

#clean-up
rm -f $trndir/_tmpf_randutt $trndir/_tmpf_tr $cvdir/_tmpf_cv

