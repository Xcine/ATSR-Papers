from dataset import DataSet

path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"
path_feats= "metadata/feats.scp"

ds = DataSet(path_spk2gender, path_segments, path_feats)
