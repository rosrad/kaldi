#!/bin/bash
. path.sh
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

# corpus_root=/home/renbo/work/corpus/uni_doa/simu/doa_360_degree_data_no_reverb/
# data_dir='./'




[ ! -d  $data_dir ] & mkdir -p $data_dir

echo "for $data_dir/wav.scp"
find $corpus_root -type f  -iname  "*.wav"|sort \
    | perl -ane 'm/(degree_\d+.*)\.wav$/; $utt=$1; $utt =~ tr#/.#_#; print "$utt \t $_";' \
    > $data_dir/wav.scp
wc $data_dir/wav.scp



echo "for $data_dir/utt2doa"
cat $data_dir/wav.scp \
    | perl -ane 'my @array = split(/ /); $array[0] =~ m/degree_(\d+)/; $n=int($array[0]/5); print "$n \t $1\n";' \
    > $data_dir/utt2doa
wc $data_dir/utt2doa

cp $data_dir/utt2doa $data_dir/utt2spk
utils/utt2spk_to_spk2utt.pl $data_dir/utt2spk > $data_dir/spk2utt 
