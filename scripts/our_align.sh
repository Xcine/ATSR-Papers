train_cmd="utils/run.pl"
decode_cmd="utils/run.pl"
path="exp/train_yesno_mono"

steps/align_fmllr.sh --nj 1 --cmd "$train_cmd" \
	data/train_yesno data/lang exp/mono0a exp/train_yesno_mono

gunzip -c $path/ali.1.gz > $path/ali.1 

ali-to-phones --ctm-output $path/final.mdl ark:$path/ali.1 $path/ctm.1

utils/int2sym.pl -f 5 $path/phones.txt $path/ctm.1 > $path/ctmp.1
