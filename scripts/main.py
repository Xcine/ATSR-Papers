import pandas as pd
import numpy as np
import re

path = "../data/malfong/train/"
path_audio = "../data/audio/"
path_utt2spk = "../data/malfong/train/utt2spk"

string1 = "/usr/bin/sox "
string2 = " -t wav -r 8000 -c 1 - remix 2|\n"

file_utt2spk = open(path_utt2spk, 'r')
line_utt2spk = file_utt2spk.readlines()
line_utt2spk_clean = [re.sub(r'.*rad', 'rad', line).split("_")[0] + "\n" for line in line_utt2spk]
line_utt2spk = [line.split(" ")[0].split("_")[0] + "\n" for line in line_utt2spk]


#file = open(path, 'r')
#lines = file.readlines()
lines = [line.replace("\n","") + " " + string1 + path_audio + re.sub(r'.*rad', 'rad', line).replace("\n","") + ".mp3" + string2 for line in line_utt2spk]

file2 = open(path+'wav.scp', 'w')
file2.writelines((lines))
file2.close()