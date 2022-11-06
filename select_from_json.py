import os
import pandas as pd
import json
from shutil import copyfile
import numpy as np
import math

with open("raw/3d_detection/VoxelNet/infos_train_10sweeps_withvelo_filter_True.json",'r') as load_f1:
    load_dict1 = json.load(load_f1)
    load_dict1 = load_dict1['results'] #拆第一层花括号

with open("raw/3d_detection/VoxelNet/infos_val_10sweeps_withvelo_filter_True.json",'r') as load_f2:
    load_dict2 = json.load(load_f2)
    load_dict2 = load_dict2['results'] #拆第一层花括号


json_content = {"meta":{
                "use_camera": False,
                "use_lidar":  True,
                "use_radar":  False,
                "use_map":    False,
                "use_external": False
        }}
json_content["results"] = {}

filenames = os.listdir('raw/2d_label/imgs/CAM_FRONT')
filenames.sort()
for i in range(len(filenames)):

    # 1. 将2d label与3d detection, 3d pointcloud关联
    # 2d file -> time
    _2d_filetime = filenames[i][-20:-9]
    
    with open("sample.json",'r') as load_f:
        load_list = json.load(load_f)
        for j in range(len(load_list)):
            # time -> token
            _3d_timestamp = load_list[j]["timestamp"]
            if abs(int(str(_3d_timestamp)[0:11]) - int(_2d_filetime)) <= 1:
                # print(_3d_timestamp)
                _3d_token = load_list[j]["token"]

                for key in load_dict1:
                    if key == _3d_token:
                        json_content["results"][key] = load_dict1[key]
                        print(len(json_content["results"]))
                        break
                
                for key in load_dict2:
                    if key == _3d_token:
                        json_content["results"][key] = load_dict2[key]
                        print(len(json_content["results"]))
                        break


with open('mini-VoxelNet.json', 'w') as f:
    json.dump(json_content, f)
                