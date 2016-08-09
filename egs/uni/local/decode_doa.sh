
set -e # exit on error
. cmd.sh
. path.sh # source the path.
echo "$0 $@"  # Print the command line for logging
# ++++++++++++++++++++++++++++++++++++++++++++++++++
# parameters initialized
cmd=utils/run.pl
nj=3
. parse_options.sh || exit 1;


if [ $# != 2 ]; then
    echo "Usage: $0 <exp-dir>  <data>"
    echo " e.g.: $0 exp/doa data/eval"
    echo ""
    echo "main options (for others, see top of script file)"
    exit 1;
fi

exp_dir=$1
data=$2

nnet=$exp_dir/final.nnet
for f in $nnet $data/feats.scp $data/spk2utt ; do
    [ ! -f $f ] && echo "train_doa.sh: no such file $f" && exit 1;
done

num_spk=$(wc -l $data/spk2utt|awk '{print $1}')
nj=$(( num_spk > nj ? nj : num_spk))

if [ -f $exp_dir/final.feature_transform ] ;then
    feature_transform=$exp_dir/final.feature_transform
fi

sdata=$data/split$nj;
[[ -d $sdata && $data/feats.scp -ot $sdata ]] || utils/split_data.sh $data $nj || exit 1;



tag=$(echo $data|sed 's#/#_#g')
decode_dir=$exp_dir/decode_$tag
mkdir -p $decode_dir 


feats="scp:$sdata/JOB/feats.scp"
[ ! -d $decode_dir/split$nj ] && mkdir -p $decode_dir/split$nj/

$cmd JOB=1:$nj $decode_dir/log/decode.JOB.log \
    nnet-forward --apply-log --feature-transform=$feature_transform --use-gpu="yes" \
    "$nnet" "$feats" ark:- \| max-prob ark:- ark,t:$decode_dir/split$nj/decode.JOB.result

cat $decode_dir/split$nj/decode.*.result > $decode_dir/decode.result
rm $decode_dir/split$nj -fr

# compute doa recognition err rate
err=$(./local/compute_er.py $decode_dir/decode.result $data/utt2doa)
echo $data : $err
