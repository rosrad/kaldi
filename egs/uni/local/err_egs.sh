#!/usr/bin/env bash

if [[ $# < 2 ]] ;then
    echo "No enough args ! "
    echo "Usage: $0 decode_dir data_dir"
    exit 1
fi

dir=$1
data=$2

for d in $dir $data
do
    if [ ! -d $d ] ;then
        echo "No exist input dir : $d ..."
        exit 1;
    fi
done
for f in decode.result err.keys
do
    if [[ ! -f $dir/$f ]] ;then
        echo "$dir/$f  not exist ! "
        exit 1;
    fi
done

./utils/filter_scp.pl --exclude $dir/err.keys $data/utt2spk \
    |awk '{print $1}' | shuf - |head -n 20 > $dir/correct.keys

for tag in err correct
do
    echo "----------------------------------------------"
    echo "working on ..."
    echo "$tag"
    echo "$dir"
    echo "----------------------------------------------"

    key=${tag}.keys
    tag_dir=$dir/${tag}

    [ ! -d $tag_dir ] && mkdir $tag_dir
    ./utils/filter_scp.pl $dir/${key} $dir/decode.result > $tag_dir/${tag}.result


    for f in feats.scp segments utt2spk utt2doa
    do
        [ ! -f $data/$f ] && continue # if not such file, skip it;
        # if exist filter it by error keys
        # echo "filtering $f"
        ./utils/filter_scp.pl $dir/${key} $data/$f > $tag_dir/$f
    done

    # cp $data/wav.scp $tag_dir/wav.scp

    # extract err  wavfiles
    wav_dir=$tag_dir/wav
    [ ! -d $wav_dir ] && mkdir $wav_dir

    if [ -f $tag_dir/segments ] ;then
        extract-segments scp:$data/wav.scp $tag_dir/segments ark:- \
            | wav-to-dir ark:- $wav_dir
    else
        ./utils/filter_scp.pl $dir/${key} $data/wav.scp \
            | wav-to-dir scp:- $wav_dir
    fi

    # extract features

    feat_dir=$tag_dir/feat
    [ ! -d $feat_dir ] && mkdir $feat_dir
    copy-feats scp:$tag_dir/feats.scp ark,scp:$feat_dir/err_feats.ark,$feat_dir/err_feats.scp

done
