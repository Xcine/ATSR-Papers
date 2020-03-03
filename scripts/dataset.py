import re
import numpy as np
import pandas as pd

class DataSet:
    def __init__(self, path_spk2gender, path_segments, path_feats, ctm_path):
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

        with open(output_feats_path, "w") as f:
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

    def select_data_of_number_spkr(self, output_feats_path, nb_spkr=5, time=1):

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

        with open(output_feats_path, "w") as f:
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

    def get_label(self, hour):
        if (hour >= 22 or hour <= 5):
            return 1
        elif (hour >= 9 and hour <= 18):
            return 0


    def get_mean_duration(self):
        mean_duration_n = np.mean([row["duration"] for i,row in self.ctm_data.iterrows() if row["sd label"] == 0])
        mean_duration_sd = np.mean([row["duration"] for i,row in self.ctm_data.iterrows() if row["sd label"] == 1])

        return mean_duration_n,mean_duration_sd

    def get_mean_of_all_phonemes(self):
        phoneme_list = {}

        for i,row in self.ctm_data.iterrows():
            key = row["phoneme"] #+ "_" + str(bool(row["sd label"]))
            if key in phoneme_list.keys():
                phoneme_list[key].append([row["duration"],row["sd label"]])
            else:
                phoneme_list[key] = [[row["duration"],row["sd label"]]]

        means_list = []
        for key in phoneme_list.keys():

            sd_list = [x[0] for x in phoneme_list[key] if x[1] == 1]
            n_list = [x[0] for x in phoneme_list[key] if x[1] == 0]

            if(len(sd_list)!=0 and len(n_list)!=0):
                means_list.append([key, float(np.mean(n_list)), float(np.mean(sd_list))])
            #print(key, np.mean(n_list), np.mean(sd_list))



        return means_list



