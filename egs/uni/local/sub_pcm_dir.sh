#!/bin/bash
set -e # exit on error
. cmd.sh
. path.sh # source the path.
nchan=1
sample_rate=16000
echo "$0 $@"  # Print the command line for logging

. utils/parse_options.sh || exit 1;
if [ $# != 2 ]; then
    echo "Usage: $0 <src> <dest>"
    echo " e.g.: $0 20151010 vad"
    echo ""
    echo "main options (for others, see top of script file)"
    echo "  --nchan <N>         # number of pcm channel"
    echo "  --sample-rate <N>   # sampling rate of pcm"
    exit 1;
fi

src=$1
dest=$2

for pcm in $(find $src -type f  -iname  "*.pcm"|sort)
do
    echo $pcm
    dest_pcm=${pcm/$src/$dest/}
    echo $dest_pcm
    txt=${pcm/.pcm/.txt}
    ./local/vad/pcm2vad.sh --nchan $nchan $pcm $txt >/dev/null 
    seg=$(head -n2 $txt|tail -n 1)
    echo utils/io/sub_pcm $seg  $pcm $dest_pcm
    dir=$(dirname $dest_pcm)
    [ ! -d $dir ] && mkdir -p $dir

    utils/io/sub_pcm $seg  $pcm $dest_pcm
done
