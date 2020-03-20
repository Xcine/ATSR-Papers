import re
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from os import path
import collections
from matplotlib.lines import Line2D

class DataSet:
    def __init__(self, path_spk2gender, path_segments, path_feats, ctm_path):
        self.ctm_id = ctm_path.split(".")[0]

        file_seg = open(path_segments, 'r')
        line_seg = file_seg.readlines()
        self.seg_id = [line.split(" ")[0] for line in line_seg]
        line_seg = [re.sub(r'.*rad', '', line).split("_")[0] for line in line_seg]
        line_seg = [line.split("_")[0] for line in line_seg]
        line_name_seg = [line.split(" ")[0] for line in line_seg]
        self.line_time_dif = [float(line.split(" ")[2]) - float(line.split(" ")[1]) for line in line_seg]

        self.id2dif = []
        last_name = line_name_seg[0]
        sum = 0

        for name, time_dif in zip(line_name_seg, self.line_time_dif):
            if (name == last_name):
                sum += time_dif
            else:
                self.id2dif.append([last_name, sum])
                last_name = name
                sum = time_dif

        self.hour2dif = []
        last_name = line_name_seg[0]
        sum = 0

        for name, time_dif in zip(line_name_seg, self.line_time_dif):
            if (name == last_name):
                sum += time_dif
            else:
                self.hour2dif.append([int(last_name[9:11]), sum])
                last_name = name
                sum = time_dif

        file_feats = open(path_feats, 'r')
        self.line_feats = file_feats.readlines()
        self.id_feats = [line.split(" ")[0] for line in self.line_feats]
        self.line_feats_clean = [re.sub(r'.*rad', '', line).split("_")[0] for line in self.line_feats]

        #-----------------------------

        self.ctm_data = pd.read_csv(ctm_path, sep=" ", header=None, names=["ID","channel","starttime","duration","phoneme", "X"])
        self.ctm_data.pop("channel")
        self.ctm_data.pop("X")
        self.ctm_data["sd label"] = [self.get_label(int(re.sub(r'.*rad', '', line).split("_")[0][9:11])) for line in self.ctm_data["ID"]]
        #print(self.ctm_data)


    def select_data(self, output_feats_path, time=1):

        time_collected_sd = 0
        time_collected_n = 0

        with open(output_feats_path, "w") as f:
            for i,line in enumerate(self.line_feats):

                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])


                if (hour >= 22 or hour <= 5) and time_collected_sd <= time*3600:
                    f.write(line)
                    time_collected_sd += self.line_time_dif[i]
                elif (hour >= 9 and hour <= 18) and time_collected_n <= time*3600:
                    f.write(line)
                    time_collected_n += self.line_time_dif[i]

        print("Written " + str(time_collected_sd) + "s of sleep deprication data to " + output_feats_path)
        print("Written " + str(time_collected_n) + "s of normal data to " + output_feats_path)

    def select_data_same_spkr(self, output_feats_path, time=1):

        time_collected_sd = 0
        time_collected_n = 0

        collected_sd = {}

        with open(output_feats_path, "w") as f:
            for i,line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour >= 22 or hour <= 5) and time_collected_sd <= time*3600:
                    f.write(line)
                    time_collected_sd += self.line_time_dif[i]
                    if spkr in collected_sd.keys():
                        collected_sd[spkr] += self.line_time_dif[i]
                    else:
                        collected_sd[spkr] = self.line_time_dif[i]

            print(collected_sd)

            for i, line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour >= 9 and hour <= 18) and (time_collected_n <= time * 3600) and spkr in collected_sd.keys():

                    if collected_sd[spkr] > 0:
                        f.write(line)
                        time_collected_n += self.line_time_dif[i]
                        collected_sd[spkr] -= self.line_time_dif[i]

        print("Written " + str(time_collected_sd) + "s of sleep deprication data to " + output_feats_path)
        print("Written " + str(time_collected_n) + "s of normal data to " + output_feats_path)


    def select_data_max_spkr(self, output_feats_path):

        time_collected_sd = 0
        time_collected_n = 0

        collected_sd = {}
        collected_sd_max = {}

        with open(output_feats_path, "w") as f:
            for i,line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour <= 5 or hour >= 23):
                    if spkr in collected_sd.keys():
                        collected_sd[spkr] += self.line_time_dif[i]
                    else:
                        collected_sd[spkr] = self.line_time_dif[i]

            max_spkr = max(collected_sd, key=collected_sd.get)
            max_value = max(collected_sd.values())
            print("max spkr + value: ", max_spkr, max_value)

            for i, line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour >= 23 or hour <= 5) and spkr==max_spkr:
                    f.write(line)
                    time_collected_sd += self.line_time_dif[i]
                    if spkr in collected_sd_max.keys():
                        collected_sd_max[spkr] += self.line_time_dif[i]
                    else:
                        collected_sd_max[spkr] = self.line_time_dif[i]

            print(collected_sd_max)

            for i, line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour >= 8 and hour <= 13) and spkr in collected_sd_max.keys():

                    if collected_sd_max[spkr] > 0:
                        f.write(line)
                        time_collected_n += self.line_time_dif[i]
                        collected_sd_max[spkr] -= self.line_time_dif[i]

        print("Written " + str(time_collected_sd) + "s of sleep deprication data to " + output_feats_path)
        print("Written " + str(time_collected_n) + "s of normal data to " + output_feats_path)


    def select_data_max_spkr_WER(self, output_feats_path_sd, output_feats_path_n):

        time_collected_sd = 0
        time_collected_n = 0

        collected_sd = {}
        collected_sd_max = {}

        with open(output_feats_path_sd, "w") as f:
            for i,line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour <= 5 or hour >= 23):
                    if spkr in collected_sd.keys():
                        collected_sd[spkr] += self.line_time_dif[i]
                    else:
                        collected_sd[spkr] = self.line_time_dif[i]

            max_spkr = max(collected_sd, key=collected_sd.get)
            max_value = max(collected_sd.values())
            print("max spkr + value: ", max_spkr, max_value)

            for i, line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour >= 23 or hour <= 5) and spkr==max_spkr:
                    f.write(line)
                    time_collected_sd += self.line_time_dif[i]
                    if spkr in collected_sd_max.keys():
                        collected_sd_max[spkr] += self.line_time_dif[i]
                    else:
                        collected_sd_max[spkr] = self.line_time_dif[i]

            print(collected_sd_max)

        with open(output_feats_path_n, "w") as f:

            for i, line in enumerate(self.line_feats):

                spkr = line.split("-")[0]
                line_feats_clean = re.sub(r'.*rad', '', line).split("_")[0]
                hour = int(line_feats_clean[9:11])

                if (hour >= 8 and hour <= 13) and spkr in collected_sd_max.keys():

                    if collected_sd_max[spkr] > 0:
                        f.write(line)
                        time_collected_n += self.line_time_dif[i]
                        collected_sd_max[spkr] -= self.line_time_dif[i]

        print("Written " + str(time_collected_sd) + "s of sleep deprication data to " + output_feats_path_sd)
        print("Written " + str(time_collected_n) + "s of normal data to " + output_feats_path_n)


    def get_label(self, hour):
        if (hour >= 22 or hour <= 5):
            return 1
        elif (hour >= 9 and hour <= 18):
            return 0

    def get_mean_duration(self, use_mono_phone, use_sil, all_sils):

        """
        if(path.exists(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl")):
            self.pickle_data = pickle.load(open(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl", "rb"))
            return self.pickle_data["mean_dur_n"], self.pickle_data["mean_dur_sd"],self.pickle_data["var_dur_n"], self.pickle_data["var_dur_sd"]
        else:
            if use_sil:
                if all_sils:
                    mean_list_n = [row["duration"] for i,row in self.ctm_data.iterrows() if (row["sd label"] == 0)]
                    mean_list_sd = [row["duration"] for i,row in self.ctm_data.iterrows() if (row["sd label"] == 1)]
                    mean_duration_n = np.mean(mean_list_n)
                    mean_duration_sd = np.mean(mean_list_sd)
                    var_duration_n = np.var(mean_list_n)
                    var_duration_sd = np.var(mean_list_sd)
                    return mean_duration_n,mean_duration_sd,var_duration_n,var_duration_sd
                else:
                    raise ValueError("not implemented yet")
            else:
                mean_list_n = [row["duration"] for i, row in self.ctm_data.iterrows() if (row["sd label"] == 0 and row["phoneme" != "sil"])]
                mean_list_sd = [row["duration"] for i, row in self.ctm_data.iterrows() if (row["sd label"] == 1 and row["phoneme" != "sil"])]
                mean_duration_n = np.mean(mean_list_n)
                mean_duration_sd = np.mean(mean_list_sd)
                var_duration_n = np.var(mean_list_n)
                var_duration_sd = np.var(mean_list_sd)
                return mean_duration_n, mean_duration_sd, var_duration_n, var_duration_sd
        """

        if(path.exists(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl")):
            self.pickle_data = pickle.load(open(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl", "rb"))
            phoneme_list = self.pickle_data["phoneme_list"]
            sd_list = []
            n_list = []
            for key in phoneme_list.keys():
                sd_list += [x[0] for x in phoneme_list[key] if x[1] == 1]
                n_list += [x[0] for x in phoneme_list[key] if x[1] == 0]

            mean_duration_n = np.mean(n_list)
            mean_duration_sd = np.mean(sd_list)
            var_duration_n = np.var(n_list)
            var_duration_sd = np.var(sd_list)
            return mean_duration_n, mean_duration_sd, var_duration_n, var_duration_sd
        else:
            raise ValueError("run get_mean_of_all_phonemes() first!")


    def get_mean_of_all_phonemes(self, use_mono_phone, use_sil, all_sils):

        if(path.exists(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl")):
            self.pickle_data = pickle.load(open(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl", "rb"))
            print("oov instances sd: ", self.pickle_data["oov_sd"])
            print("oov instances n: ", self.pickle_data["oov_n"])
            return self.pickle_data["means_phoneme_list"], self.pickle_data["phoneme_list"]
        else:
            phoneme_list = {}
            last_sil_ind = self.ctm_data["ID"][0].split("_")[1]
            for i,row in self.ctm_data.iterrows():
                cur_sil_ind = row["ID"].split("_")[1]
                if all_sils or ((i != 0) and (cur_sil_ind == last_sil_ind)):
                    if use_mono_phone:
                        key = row["phoneme"].split("_")[0]
                    else:
                        key = row["phoneme"]
                    if key in phoneme_list.keys():# and (not ("oov" in key)):
                        phoneme_list[key].append([row["duration"],row["sd label"]])
                    elif use_sil or (not use_sil and key != "sil"):
                            phoneme_list[key] = [[row["duration"],row["sd label"]]]
                else:
                    last_sil_ind = cur_sil_ind

            means_list = []
            for key in phoneme_list.keys():

                sd_list = [x[0] for x in phoneme_list[key] if x[1] == 1]
                n_list = [x[0] for x in phoneme_list[key] if x[1] == 0]

                if "oov" in key:
                    print(key)
                    oov_sd = len(sd_list)
                    oov_n = len(n_list)
                    print("oov instances sd: ", len(sd_list))
                    print("oov instances n: ", len(n_list))
                elif (len(sd_list)!=0 and len(n_list)!=0):
                    means_list.append([key, float(np.mean(n_list)), float(np.mean(sd_list)),float(np.var(n_list)), float(np.var(sd_list))])

            phoneme_list.pop('oov', None)
            phoneme_list.pop('oov_S', None)
            phoneme_list.pop('oov_E', None)
            phoneme_list.pop('oov_I', None)
            pickel_data = {"means_phoneme_list": means_list, "phoneme_list": phoneme_list, "oov_sd": oov_sd, "oov_n": oov_n}
            pickle.dump(pickel_data, open(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(use_sil)) + "_" + str(int(all_sils)) + ".pkl", "wb"))

            return means_list, phoneme_list


    def analyse_sil(self, all_sils):

        for use_mono_phone in [True,False]:

            if(path.exists(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(True)) + "_" + str(int(all_sils)) + ".pkl")):
                self.pickle_data = pickle.load(open(self.ctm_id + "_" + str(int(use_mono_phone)) + "_" + str(int(True)) + "_" + str(int(all_sils)) + ".pkl", "rb"))
                phoneme_list = self.pickle_data["phoneme_list"]
                sd_list = []
                n_list = []
                for key in phoneme_list.keys():
                    sd_list += [x[0] for x in phoneme_list[key] if (x[1] == 1 and key == "sil")]
                    n_list += [x[0] for x in phoneme_list[key] if (x[1] == 0  and key == "sil")]

                mean_duration_n = np.mean(n_list)
                mean_duration_sd = np.mean(sd_list)
                var_duration_n = np.var(n_list)
                var_duration_sd = np.var(sd_list)
                return n_list, sd_list, mean_duration_n, mean_duration_sd, var_duration_n, var_duration_sd
            else:
                raise ValueError("run get_mean_of_all_phonemes() first!")


    def analyse_speaker_dist(self, path_ctm_spkr):

        ctm_spkr = pd.read_csv(path_ctm_spkr, sep=" ", header=None, names=["ID","channel","starttime","duration","phoneme", "X"])
        ctm_spkr.pop("channel")
        ctm_spkr.pop("X")
        ctm_spkr["sd label"] = [self.get_label(int(re.sub(r'.*rad', '', line).split("_")[0][9:11])) for line in ctm_spkr["ID"]]
        ctm_spkr["hour"] = [int(re.sub(r'.*rad', '', line).split("_")[0][9:11]) for line in ctm_spkr["ID"]]
        spkr_id = ctm_spkr["ID"][0].split("-")[0]

        time_sd = np.sum([row["duration"] for i,row in ctm_spkr.iterrows() if (row["sd label"] == 1)])
        time_n = np.sum([row["duration"] for i, row in ctm_spkr.iterrows() if (row["sd label"] == 0)])
        print("Speaker: ", spkr_id)
        print("Time in seconds of normal state: ", time_n)
        print("Time in seconds of sleep deprivation: ", time_sd)

        hours_dict = {}
        for i, row in ctm_spkr.iterrows():
            key = row["hour"]
            if key in hours_dict.keys():
                hours_dict[key] += row["duration"]
            else:
                hours_dict[key] = row["duration"]

        hours_dict = sorted(hours_dict.items())
        x, y = zip(*hours_dict)

        colors = []
        for key in x:
            if self.get_label(key)==1:
                colors.append("red")
            else:
                colors.append("green")

        ax = plt.subplot(111)
        plt.bar(x,y, color = colors)
        plt.xlabel("Speech Start of the Day (Only the Hour)")
        plt.ylabel("Duration of Spoken Time in seconds")
        plt.xticks(np.arange(0, 24, 2))

        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Sleep Deprivation',
                                  markerfacecolor='r', markersize=15),
                           Line2D([0], [0], marker='o', color='w', label='Normal',
                                  markerfacecolor='g', markersize=15)]
        ax.legend(handles=legend_elements, loc='upper right')
        plt.savefig("graphs/meta_" + spkr_id + ".pdf")







