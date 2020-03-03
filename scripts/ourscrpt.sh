train_cmd="utils/run.pl"
decode_cmd="utils/run.pl"

steps/decode.sh --nj 1 --cmd "$decode_cmd" \
	exp/mono0a/graph_tgpr data/test_yesno_our exp/mono0a/decode_test_yesno_our

