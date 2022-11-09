import numpy as np
import os

car_list = ['car', 'bus', 'truck', 'construction_vehicle', 'trailer', 'emergency']
pedestrian_list = ['pedestrian']
bicycle_list = ['bicycle', 'motorcycle']
moveable_object_list = ['traffic_cone', 'barrier', 'moveable_object', 'movable_object']

detection_path = 'new/3d_detection/VoxelNet/train'
filenames = os.listdir(detection_path)
filenames.sort()

for i in range(len(filenames)):
    # print(filenames[i])
    _3d_detection_path = os.path.join(detection_path, filenames[i])

    with open(_3d_detection_path, 'r') as f:
        lines = f.readlines()
    
    content_3d = []
    for line in lines:
        line = line.replace(",", "")
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.replace("\n", "")
        
        content_3d.append(line)

    content_3d = [line.strip().split(' ') for line in content_3d]

    new_content = ''
    # 最后一行是token
    for j in range(len(content_3d)-1):
        if content_3d[j][0] in car_list:
            content_3d[j][0] = 'car'
        elif content_3d[j][0] in pedestrian_list:
            content_3d[j][0] = 'pedestrian'
        elif content_3d[j][0] in bicycle_list:
            content_3d[j][0] = 'bicycle'
        elif content_3d[j][0] in moveable_object_list:
            content_3d[j][0] = 'movable_object'
        else:
            print(content_3d[j][0])
        
        for k in range(len(content_3d[j])):
            new_content = new_content + str(content_3d[j][k]) + ' '
        
        new_content = new_content + '\n'
    
    # 把最后一行token加上
    new_content = new_content + str(content_3d[-1][0])

    _3d_file = open('new/3d_detection/VoxelNet/new/{}.txt'.format(filenames[i][:-4]), 'w')
    _3d_file.write(new_content)
    _3d_file.close()

    print(filenames[i][:-4])





