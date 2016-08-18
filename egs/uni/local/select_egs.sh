#!/usr/bin/env bash

dir=$1
egs_dir=${dir%/}_egs
[ -z $egs_dir ] && echo 'egs_dir cannot be empty' && exit 1;
# clean up egs_dir
[ -d  $egs_dir ] && rm -fr $egs_dir/*
[ ! -d  $egs_dir ] && mkdir $egs_dir

for d in $(find $dir  -maxdepth 1 -type d )
do
    [ ! -f $d/wav.scp ] && continue
    [ ! -f $d/spk2utt ] && continue
    awk 'BEGIN{OFS="\n"}{print $2,$3}' $d/spk2utt >> $egs_dir/keys
    cat $d/segments >>$egs_dir/segments
    cat $d/wav.scp >> $egs_dir/wav.scp
done

utils/filter_scp.pl $egs_dir/keys $egs_dir/segments > $egs_dir/egs.segments
extract-segments scp:$egs_dir/wav.scp $egs_dir/egs.segments ark,scp:$egs_dir/egs_wav.ark,$egs_dir/egs_wav.scp
cp $egs_dir/egs_wav.scp ${dir%/}_egs.scp
