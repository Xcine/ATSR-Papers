from dataset import DataSet
import matplotlib.pyplot as plt
import numpy as np

path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"
path_feats= "metadata/feats/feats.scp"
path_ctm = "metadata/ctm/allp_train_max_spk_i2.ctm"

ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)

ds.analyse_speaker_dist(path_ctm)

