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
#path_utt2spk = "../data/malfong/train/utt2spk"
path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"

#getting utt and speaking times
file_utt2spk = open(path_utt2spk, 'r')
line_utt2spk = file_utt2spk.readlines()
line_utt2spk_clean = [re.sub(r'.*rad', '', line).split("_")[0] for line in line_utt2spk]

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
    if(x >=22 or x <= 5):
        i+=1
print("Number of utterances: ",len(hours))
print("Number of utterances from 21:00 - 6:00: ",i)

#plot data for utt and speaking hour
plt.hist(hours, bins=20)
plt.xlabel("Speech Start of the Day (Only the Hour)")
plt.ylabel("Number of Utterances (190000 of Total Utterances)")
plt.savefig("graphs/meta.pdf")

#getting gender data
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

#getting speaking lengths
file_seg = open(path_segments, 'r')
line_seg = file_seg.readlines()
line_seg = [re.sub(r'.*rad', '', line).split("_")[0] for line in line_seg]
line_seg = [line.split("_")[0] for line in line_seg]
line_name_seg = [line.split(" ")[0] for line in line_seg]
line_time_dif = [float(line.split(" ")[2])-float(line.split(" ")[1]) for line in line_seg]

id2dif = []
last_name = line_name_seg[0]
sum = 0

for name,time_dif in zip(line_name_seg,line_time_dif):
    if(name == last_name):
        sum += time_dif
    else:
        id2dif.append([last_name, sum])
        last_name = name
        sum = time_dif

hours = [int(line[9:11]) for line in np.array(id2dif)[:,0]]

hour2dif = []
last_name = line_name_seg[0]
sum = 0

for name,time_dif in zip(line_name_seg,line_time_dif):
    if(name == last_name):
        sum += time_dif
    else:
        hour2dif.append([int(last_name[9:11]), sum])
        last_name = name
        sum = time_dif

time_dif_normal = 0
time_dif_sleep_depri = 0
for hour,time_dif in hour2dif:
    if(hour>=22 or hour<=5):
        time_dif_sleep_depri += time_dif
    else:
        time_dif_normal += time_dif

hours_sd = time_dif_sleep_depri/(60.0*60.0)
hours_nm = time_dif_normal/(60.0*60.0)

print("Hours of sleep deprivation (22:00-6:00): ", hours_sd)
print("Hours of normal speech: ", hours_nm)









