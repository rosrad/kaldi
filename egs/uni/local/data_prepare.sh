#!/bin/bash
. path.sh
nchan=4;
fs=16000;
bits=16;
pcm2wav=${KALDI_ROOT}/tools/pcm2wav/pcm2wav
nlog=2
. parse_options.sh || exit 1;

if [ $# -ne 2 ]; then
    echo "USAGE: %0 [opts] <corpus_root> <data_dir>"
    echo "Options: "
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

echo  $data_dir/segments
for f in $files
do
    name=$(basename $f);
    cat $f |awk -v r=${name%.*} '{print  r"_"$1, r, $1,$2} '
done |tee $data_dir/segments |head -n $nlog


# for wav.scp
echo  $data_dir/wav.scp
for f in $files
do
    name=$(basename $f);
    echo "${name%.*} $pcm2wav ${f/%.txt/.pcm} - $nchan $fs $bits |"
done |tee $data_dir/wav.scp |head -n $nlog

