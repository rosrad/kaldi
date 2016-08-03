#!/bin/bash

# Copyright 2012-2016  Johns Hopkins University (Author: Daniel Povey)
# Apache 2.0
# To be run from .. (one directory up from here)
# see ../run.sh for example

# Begin configuration section.
nj=8
cmd=run.pl
gcc_config=conf/gcc.conf
# End configuration section.

echo "$0 $@"  # Print the command line for logging

if [ -f path.sh ]; then . ./path.sh; fi
. parse_options.sh || exit 1;

if [ $# -lt 1 ] || [ $# -gt 3 ]; then
    echo "Usage: $0 [options] <data-dir> [<log-dir> [<gcc-dir>] ]";
    echo "e.g.: $0 data/train exp/make_gcc/train gcc"
    echo "Note: <log-dir> defaults to <data-dir>/log, and <gccdir> defaults to <data-dir>/data"
    echo "Options: "
    echo "  --gcc-config <config-file>                      # config passed to compute-gcc-feats "
    echo "  --nj <nj>                                        # number of parallel jobs"
    echo "  --cmd (utils/run.pl|utils/queue.pl <queue opts>) # how to run jobs."
    exit 1;
fi

data=$1
if [ $# -ge 2 ]; then
    logdir=$2
else
    logdir=$data/log
fi
if [ $# -ge 3 ]; then
    gccdir=$3
else
    gccdir=$data/data
fi

# make $gccdir an absolute pathname.
gccdir=`perl -e '($dir,$pwd)= @ARGV; if($dir!~m:^/:) { $dir = "$pwd/$dir"; } print $dir; ' $gccdir ${PWD}`

# use "name" as part of name of the archive.
name=`basename $data`

mkdir -p $gccdir || exit 1;
mkdir -p $logdir || exit 1;

if [ -f $data/feats.scp ]; then
    mkdir -p $data/.backup
    echo "$0: moving $data/feats.scp to $data/.backup"
    mv $data/feats.scp $data/.backup
fi

scp=$data/wav.scp

required="$scp $gcc_config"

for f in $required; do
    if [ ! -f $f ]; then
        echo "make_gcc.sh: no such file $f"
        exit 1;
    fi
done
# utils/validate_data_dir.sh --no-text --no-feats $data || exit 1;

for n in $(seq $nj); do
    # the next command does nothing unless $gccdir/storage/ exists, see
    # utils/create_data_link.pl for more info.
    utils/create_data_link.pl $gccdir/raw_gcc_$name.$n.ark
done


if [ ! -f $data/segments ]; then
    echo "$0 [error]: no segments file for extraction"
    exit 1
fi
echo "$0 [info]: segments file exists: using that."

split_segments=""
for n in $(seq $nj); do
    split_segments="$split_segments $logdir/segments.$n"
done

utils/split_scp.pl $data/segments $split_segments || exit 1;
rm $logdir/.error 2>/dev/null

$cmd JOB=1:$nj $logdir/make_gcc_${name}.JOB.log \
    extract-segments scp,p:$scp $logdir/segments.JOB ark:- \| \
    compute-gcc --config=$gcc_config ark:- \
    ark,scp:$gccdir/raw_gcc_$name.JOB.ark,$gccdir/raw_gcc_$name.JOB.scp \
    || exit 1;


if [ -f $logdir/.error.$name ]; then
    echo "Error producing gcc features for $name:"
    tail $logdir/make_gcc_${name}.1.log
    exit 1;
fi

# concatenate the .scp files together.
for n in $(seq $nj); do
    cat $gccdir/raw_gcc_$name.$n.scp || exit 1;
done > $data/feats.scp

# rm $logdir/wav_${name}.*.scp  $logdir/segments.* 2>/dev/null

nf=`cat $data/feats.scp | wc -l`

echo "creating [$nf] GCC features for $name"
