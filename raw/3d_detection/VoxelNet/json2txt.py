import pandas as pd
import json

with open("infos_train_10sweeps_withvelo_filter_True.json",'r') as load_f:
    load_dict = json.load(load_f)
    load_dict = load_dict['results'] #拆第一层花括号

    for key in load_dict:
        # 如果file_name不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        file_name = 'train/{}.txt'.format(key)
        with open(file_name,'w') as f: 
            for i in range(len(load_dict[key])):
                f.write("{} {} {} {} {} {}\n".format(load_dict[key][i]['detection_name'], 
                                                     load_dict[key][i]['translation'],
                                                     load_dict[key][i]['rotation'],
                                                     load_dict[key][i]['size'],
                                                     load_dict[key][i]['velocity'],
                                                     load_dict[key][i]['detection_score']))
        
        f.close()


