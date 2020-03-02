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

ds = DataSet(path_spk2gender, path_segments, path_feats)

ds.select_data(path_featsx, time=2)

