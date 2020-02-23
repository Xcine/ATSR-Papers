import pandas as pd
import numpy as np
import re
import datetime
import matplotlib.pyplot as plt

#path = "../data/malfong/train/"
#path_audio = "../data/audio/"
#path_utt2spk = "../data/malfong/train/utt2spk"
path_utt2spk = "utt2spk"
path_spk2gender = "spk2gender"

file_utt2spk = open(path_utt2spk, 'r')
line_utt2spk = file_utt2spk.readlines()
line_utt2spk_clean = [re.sub(r'.*rad', '', line).split("_")[0] for line in line_utt2spk]

file_spk2gender = open(path_spk2gender, 'r')
line_spk2gender = file_spk2gender.readlines()

gender = [line[-2] for line in line_spk2gender]
females = 0
males = 0
for g in gender:
    if(g=="f"):
        females+=1
    else:
        males+=1

print("f: ",females)
print("m: ", males)

years = [int(line[0:4]) for line in line_utt2spk_clean]
months = [int(line[4:6]) for line in line_utt2spk_clean]
days = [int(line[6:8]) for line in line_utt2spk_clean]
hours = [int(line[9:11]) for line in line_utt2spk_clean]
minutes = [int(line[11:13]) for line in line_utt2spk_clean]
seconds = [int(line[13:15]) for line in line_utt2spk_clean]

"""
#check errors in input
for x in years:
    if(x<2000 or x >2020):
        print(x)

for x in months:
    if(x<1 or x >12):
        print(x)

for x in days:
    if(x<1 or x >31):
        print(x)

for x in hours:
    if(x<0 or x >23):
        print(x)

for x in minutes:
    if(x<0 or x >59):
        print(x)

for x in seconds:
    if(x<0 or x >59):
        print(x)
"""

i = 0
for x in hours:
    if(x >19 or x < 6):
        i+=1
print("Number of utterances: ",len(hours))
print("Number of utterances after 19pm and before 6am: ",i)


plt.hist(hours, bins=20)
plt.xlabel("Speech Start of the Day (Only the Hour)")
plt.ylabel("Number of Utterances (190000 of Total Utterances)")
plt.savefig("meta.pdf")

