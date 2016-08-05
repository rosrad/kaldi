#!/bin/bash
. path.sh
nchan=4;
fs=16000;
bits=16;
pcm2wav=${KALDI_ROOT}/tools/pcm2wav/pcm2wav
nlog=2
doa=
. parse_options.sh || exit 1;

if [ $# -ne 2 ]; then
    echo "USAGE: %0 [opts] <corpus_root> <data_dir>"
    echo "Options: "
    echo "  --doa           #specify doa degree"
    echo "  --nchan         #number of channels "
    echo "  --fs            #signal sample rate"
    echo "  --bits          #bits per sample"
    echo "  --pcm2wav       #pcm2wav tools path"
    echo "  --nlog          #number log for each generated file"
    exit 1;
fi

echo "$0 $@"  # Print the command line for logging
corpus_root=$1
data_dir=$2

# corpus_root=/home/renbo/work/corpus/unisound/20151010/
# data_dir='./'


files=$(find $corpus_root -type f  -iname  "*.txt"|sort)
[ ! -d  $data_dir ] & mkdir -p $data_dir


for f in $files
do
    name=$(basename $f);
    if [ -z $doa ] ; then
        d=$(basename $(dirname $f) |perl -ane 's/\D//;print;')
    else
        d=$doa
    fi
    cat $f |awk -v r=${name%.*} -v d=$d '{print  r"_"$1, r, $1,$2,d}'
done> $data_dir/tmp.scp

echo  $data_dir/segments
cat $data_dir/tmp.scp | awk '{print $1,$2,$3,$4}' > $data_dir/segments
# head   $data_dir/segments

echo  $data_dir/utt2doa
cat $data_dir/tmp.scp | awk '{print $1,$5}' > $data_dir/utt2doa

# make fake utt2spk from doa.scp
cp $data_dir/utt2doa $data_dir/utt2spk
utils/utt2spk_to_spk2utt.pl $data_dir/utt2spk > $data_dir/spk2utt 
# head $data_dir/utt2doa

rm $data_dir/tmp.scp

# for wav.scp
echo  $data_dir/wav.scp
for f in $files
do
    name=$(basename $f);
    echo "${name%.*} $pcm2wav ${f/%.txt/.pcm} - $nchan $fs $bits |"
done |sort -k1 > $data_dir/wav.scp

