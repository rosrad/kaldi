#!/usr/bin/bash
nchan=4
. utils/parse_options.sh || exit 1;

if [[ $# < 1 ]] ;then
    echo 'usage : pcm2vad.sh /dir/test.pcm [dir/test.txt]'
    exit 1
fi

pcm=$1
txt=${pcm/.pcm/.txt}

if [[ $# > 2 ]] ; then
    txt=$2
fi

exe=./local/vad/vad_lab_${nchan}ch.exe

chmod u+x ${exe}

echo ${exe} $pcm $txt
${exe} $pcm $txt




