from dataset import DataSet
import matplotlib.pyplot as plt
import numpy as np

path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"
path_feats= "metadata/feats/feats.scp"
#path_ctm = "metadata/ctm/allp_max_spkr.ctm" #ai
#path_ctm = "metadata/ctm/allp_train_max_spk_i2.ctm" #phb
path_ctm = "metadata/ctm/allp_train_max_spk_i3.ctm" #ba

ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)

use_mono_phone=True
use_sil=True
all_sils=False
phoneme_data, phoneme_list = ds.get_mean_of_all_phonemes(use_mono_phone=use_mono_phone, use_sil=use_sil, all_sils=all_sils)
phonemes=np.array(phoneme_data)[:,0]
mean_n=np.array(phoneme_data)[:,1].astype(float)
mean_sd=np.array(phoneme_data)[:,2].astype(float)
dif = np.subtract(mean_sd, mean_n)
dif_p = sorted(zip(dif,phonemes))
print("max_spkr",dif_p)
print("max_spkr(n,sd,vn,vsd): ", ds.get_mean_duration(use_mono_phone=use_mono_phone, use_sil=use_sil, all_sils=all_sils))
x1,x2,x3,x4,x5,x6  = ds.analyse_sil(all_sils=all_sils)
print("max_spkr _sil(n,sd,vn,vsd): ", x3,x4,x5,x6)


#get boxplot data
box_value_list = []
all_box_n = []
all_box_sd = []
box_key_list = []
for key in phoneme_list.keys():

    sd_list = [x[0] for x in phoneme_list[key] if x[1] == 1]
    n_list = [x[0] for x in phoneme_list[key] if x[1] == 0]

    if "oov" in key:
        print(key)
        oov_sd = len(sd_list)
        oov_n = len(n_list)
        print("oov instances sd: ", len(sd_list))
        print("oov instances n: ", len(n_list))
    elif (len(sd_list) != 0 and len(n_list) != 0):
        box_value_list.append(n_list)
        box_key_list.append(key + " n")
        box_value_list.append(sd_list)
        box_key_list.append(key + " sd")

        all_box_n += n_list
        all_box_sd += sd_list

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
#bp = ax.boxplot(box_value_list)
#ax.set_xticklabels(box_key_list)
bp = ax.boxplot([x1,x2], showfliers=False)
ax.set_xticklabels(["SIL n", "SIL sd"])
plt.ylabel("Duration of Silence in Seconds")
plt.ylim(0,1.0)
plt.savefig("graphs/resbox_sil_BA.pdf")
plt.close()

fig = plt.figure(1, figsize=(9, 6))
ax = fig.add_subplot(111)
bp = ax.boxplot([all_box_n,all_box_sd], showfliers=False)
ax.set_xticklabels(["Phonemes n", "Phonemes sd"])
plt.ylabel("Duration of Phonemes in Seconds")
plt.ylim(0,0.2)
plt.savefig("graphs/resbox_pho_BA.pdf")

# path_ctm = "metadata/ctm/allp_same_spkrs_5h.ctm"
#
# ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)
# phoneme_data = ds.get_mean_of_all_phonemes()
# print(phoneme_data)
# phonemes=np.array(phoneme_data)[:,0]
# mean_n=np.array(phoneme_data)[:,1].astype(float)
# mean_sd=np.array(phoneme_data)[:,2].astype(float)
# dif = np.subtract(mean_sd, mean_n)
# dif_p = sorted(zip(dif,phonemes))
# print("same spkrs 5h",dif_p)
# print("same sprks 5h(n,sd,vn,vsd): ", ds.get_mean_duration())
#
#
# path_ctm = "metadata/ctm/allp_random_13h.ctm"
#
# ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)
# phoneme_data = ds.get_mean_of_all_phonemes()
# print(phoneme_data)
# phonemes=np.array(phoneme_data)[:,0]
# mean_n=np.array(phoneme_data)[:,1].astype(float)
# mean_sd=np.array(phoneme_data)[:,2].astype(float)
# dif = np.subtract(mean_sd, mean_n)
# dif_p = sorted(zip(dif,phonemes))
# print("random 13h",dif_p)
# print("random 13h(n,sd,vn,vsd): ", ds.get_mean_duration())


#plt.plot(phonemes[0:5], mean_n[0:5], 'go', phonemes[0:5], mean_sd[0:5], 'rx')
#plt.show()

