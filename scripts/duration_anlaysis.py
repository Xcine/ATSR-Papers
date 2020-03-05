from dataset import DataSet
import matplotlib.pyplot as plt
import numpy as np

path_utt2spk = "metadata/utt2spk"
path_spk2gender = "metadata/spk2gender"
path_segments = "metadata/segments"
path_feats= "metadata/feats/feats.scp"
path_ctm = "metadata/ctm/allp_random_2h.ctm"

# ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)
# phoneme_data = ds.get_mean_of_all_phonemes()
# phonemes=np.array(phoneme_data)[:,0]
# mean_n=np.array(phoneme_data)[:,1].astype(float)
# mean_sd=np.array(phoneme_data)[:,2].astype(float)
# dif = np.subtract(mean_sd, mean_n)
# dif_p = sorted(zip(dif,phonemes))
# print("random 2h",dif_p)
# print("random 2h(n,sd): ", ds.get_mean_duration())


path_ctm = "metadata/ctm/allp_same_spkrs_5h.ctm"

ds = DataSet(path_spk2gender, path_segments, path_feats, path_ctm)
phoneme_data = ds.get_mean_of_all_phonemes()
print(phoneme_data)
phonemes=np.array(phoneme_data)[:,0]
mean_n=np.array(phoneme_data)[:,1].astype(float)
mean_sd=np.array(phoneme_data)[:,2].astype(float)
dif = np.subtract(mean_sd, mean_n)
dif_p = sorted(zip(dif,phonemes))
print("same spkrs 5h",dif_p)
print("same sprks 5h(n,sd): ", ds.get_mean_duration())


#plt.plot(phonemes[0:5], mean_n[0:5], 'go', phonemes[0:5], mean_sd[0:5], 'rx')
#plt.show()

