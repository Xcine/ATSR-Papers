import pandas as pd
import numpy as np
import re
import datetime
import matplotlib.pyplot as plt

from dataset import DataSet

path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"
path_feats= "metadata/feats/feats.scp"
path_featsx= "metadata/feats/feats_max_spkr_i3.scp"
path_ctm = "metadata/ctm/allp_random_2h.ctm"

path_feats_sd = "metadata/feats/feats_max_spkr_sd_WER.scp"
path_feats_n = "metadata/feats/feats_max_spkr_n_WER.scp"

ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)

ds.select_data_max_spkr_WER(output_feats_path_sd=path_feats_sd, output_feats_path_n=path_feats_n)

