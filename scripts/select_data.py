import pandas as pd
import numpy as np
import re
import datetime
import matplotlib.pyplot as plt

from dataset import DataSet

path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"
path_feats= "metadata/feats.scp"
path_featsx= "metadata/featsx.scp"
path_ctm = "metadata/allp.ctm"

ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)

ds.select_data_same_spkr(path_featsx, time=5)

