import pandas as pd
import numpy as np
import re
import datetime
import matplotlib.pyplot as plt


def findnth(haystack, needle, n):
    parts= haystack.split(needle, n+1)
    if len(parts)<=n+1:
        return -1
    return len(haystack)-len(parts[-1])-len(needle)

#path = "../data/malfong/train/"
#path_audio = "../data/audio/"
#path_feats = "../data/malfong/train_feats"
path_feats= "metadata/feats.scp"
path_featsx= "metadata/featsx.scp"


#getting utt and speaking times
file_feats = open(path_feats, 'r')
line_feats = file_feats.readlines()
line_feats_clean = [re.sub(r'.*rad', '', line).split("_")[0] for line in line_feats]

years = [int(line[0:4]) for line in line_feats_clean]
months = [int(line[4:6]) for line in line_feats_clean]
days = [int(line[6:8]) for line in line_feats_clean]
hours = [int(line[9:11]) for line in line_feats_clean]
minutes = [int(line[11:13]) for line in line_feats_clean]
seconds = [int(line[13:15]) for line in line_feats_clean]


time_collected_sd = 0
time_collected_n = 0

with open(path_featsx, "w") as f:
    for line in line_feats:

        line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
        hour = int(line_feats_clean[9:11])

        if hour>=22 or hour<=5 and time_collected_sd <= 7200:
            f.write(line)
            time_collected_sd += 10
        elif time_collected_n <= 7200:
            f.write(line)
            time_collected_n += 10

