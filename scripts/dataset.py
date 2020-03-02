import re
import numpy as np

class DataSet:
    def __init__(self, path_spk2gender, path_segments, path_feats):
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


