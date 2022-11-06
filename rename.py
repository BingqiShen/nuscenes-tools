import os
import pandas as pd
import json
from shutil import copyfile
import numpy as np
import math

def quat_to_pos_matrix_hm(p_x, p_y, p_z, x, y, z, w):
    # 创建位姿矩阵，写入位置
    T = np.matrix([[0, 0, 0, p_x], [0, 0, 0, p_y], [0, 0, 0, p_z], [0, 0, 0, 1]])
    T[0, 0] = 1 - 2 * pow(y, 2) - 2 * pow(z, 2)
    T[0, 1] = 2 * (x * y - w * z)
    T[0, 2] = 2 * (x * z + w * y)

    T[1, 0] = 2 * (x * y + w * z)
    T[1, 1] = 1 - 2 * pow(x, 2) - 2 * pow(z, 2)
    T[1, 2] = 2 * (y * z - w * x)

    T[2, 0] = 2 * (x * z - w * y)
    T[2, 1] = 2 * (y * z + w * x)
    T[2, 2] = 1 - 2 * pow(x, 2) - 2 * pow(y, 2)
    
    return T

def rotationMatrixToEulerAngles_yaw(R) :
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
    
    singular = sy < 1e-6

    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return z


filenames = os.listdir('raw/2d_label/labels/CAM_FRONT')
filenames.sort()
for i in range(len(filenames)):
    # print(filenames[i])

    # 1. 将2d label与2d img关联
    _2d_label_path = os.path.join('raw/2d_label/labels/CAM_FRONT', filenames[i][:-4] + '.txt')
    _2d_img_path = os.path.join('raw/2d_label/imgs/CAM_FRONT', filenames[i][:-4] + '.jpg')
    try:
        copyfile(_2d_label_path, 'new/2d_label/labels/CAM_FRONT/{}.txt'.format(i))
        copyfile(_2d_img_path, 'new/2d_label/imgs/CAM_FRONT/{}.jpg'.format(i))
    except IOError as e:
        print(e)

    # 2. 将2d label与3d detection, 3d pointcloud关联
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
                _3d_filelist = os.listdir('raw/3d_detection/VoxelNet')
                for root, dirs, files in os.walk('raw/3d_detection/VoxelNet'):
                    for file in files:
                        _3d_filename = str(root) + str(dirs) + str(file)
                        # token -> 3d file
                        if _3d_token in _3d_filename:
                            _3d_path = os.path.join(root, file)
                            try:
                                copyfile(_3d_path, 'new/3d_detection/VoxelNet/bak/{}.txt'.format(i))
                            except IOError as e:
                                print(e)
                                print(_3d_path)
                            break
                
                for root, dirs, files in os.walk('raw/3d_pointcloud/LIDAR_TOP'):
                    for file in files:
                        pointcloud_filename = str(root) + str(dirs) + str(file)
                        # token -> 3d file
                        if str(_3d_timestamp) in pointcloud_filename:
                            pointcloud_path = os.path.join(root, file)
                            try:
                                copyfile(pointcloud_path, 'new/3d_pointcloud/LIDAR_TOP/{}.bin'.format(i))
                            except IOError as e:
                                print(e)
                            break
                break
    
    # 3. 将2d label与2d 标定关联
    with open("sample_data.json",'r') as load_f:
        load_list = json.load(load_f)
        for k in range(len(load_list)):
            if filenames[i][:-4] in load_list[k]["filename"]:
                calib_token = load_list[k]["calibrated_sensor_token"]
                break
    with open("calibrated_sensor.json",'r') as load_f:
        load_list = json.load(load_f)
        for l in range(len(load_list)):
            if calib_token in load_list[l]["token"]:
                cam_intrinsic = load_list[l]["camera_intrinsic"]
                cam_translation = load_list[l]["translation"]
                cam_rotation = load_list[l]["rotation"]
                # print(cam_intrinsic)
                break

    # 4. 将3d detection与3d 标定 和3d pose 关联
    with open("sample_data.json",'r') as load_f:
        load_list = json.load(load_f)
        for n in range(len(load_list)):
            if str(_3d_timestamp) in str(load_list[n]["timestamp"]):
                _3d_calib_token = load_list[n]["calibrated_sensor_token"]
                _3d_ego_token = load_list[n]["ego_pose_token"]
                break
    with open("calibrated_sensor.json",'r') as load_f:
        load_list = json.load(load_f)
        for m in range(len(load_list)):
            if _3d_calib_token in load_list[m]["token"]:
                lidar_translation = load_list[m]["translation"]
                lidar_rotation = load_list[m]["rotation"]
                # print(lidar_translation)
                break
    
    with open("ego_pose.json",'r') as load_f:
        load_list = json.load(load_f)
        for t in range(len(load_list)):
            if _3d_ego_token in load_list[t]["token"]:
                car_translation = load_list[t]["translation"]
                car_rotation = load_list[t]["rotation"]
                # print(lidar_translation)
                break
    
    T_cam = quat_to_pos_matrix_hm(cam_translation[0], cam_translation[1], cam_translation[2],
                                  cam_rotation[1], cam_rotation[2], cam_rotation[3], cam_rotation[0])
    T_lidar = quat_to_pos_matrix_hm(lidar_translation[0], lidar_translation[1], lidar_translation[2],
                                    lidar_rotation[1], lidar_rotation[2], lidar_rotation[3], lidar_rotation[0])
    
    
    T_lidar2cam = T_cam.I * T_lidar


    # 5. 写入标定txt
    calib_file = open('new/calib/{}.txt'.format(i), 'w')
    calib_file.write(str(cam_intrinsic) + '\n' + str(T_lidar2cam.tolist()))
    calib_file.close()

    # 6. 重新写入3d txt
    T_car = quat_to_pos_matrix_hm(car_translation[0], car_translation[1], car_translation[2],
                                  car_rotation[1], car_rotation[2], car_rotation[3], car_rotation[0])
    with open('new/3d_detection/VoxelNet/bak/{}.txt'.format(i), 'r') as f:
        lines = f.readlines()
    
    content_3d = ''
    for line in lines:
        line = line.replace(",", "")
        line = line.replace("[", "")
        line = line.replace("]", "")
        line = line.replace("\n", "")

        line = line.strip().split(' ')

        T_obj = quat_to_pos_matrix_hm(float(line[1]), float(line[2]), float(line[3]),
                                      float(line[5]), float(line[6]), float(line[7]), float(line[4]))
        
        T_obj2lidar = T_lidar.I * T_car.I * T_obj

        R_obj2lidar = T_obj2lidar[0:3, 0:3]
        yaw_obj2lidar = rotationMatrixToEulerAngles_yaw(R_obj2lidar)
        t_obj2lidar = T_obj2lidar[0:3, -1].T

        # print(T_obj2lidar)
        # label + translation + size + yaw + score
        line = line[0] + ' ' + str(t_obj2lidar.tolist()) + ' ' + str([float(line[8]), float(line[9]), float(line[10])]) + ' ' + str(yaw_obj2lidar) + ' ' + str(line[13]) + '\n'

        content_3d = content_3d + line

    _3d_file = open('new/3d_detection/VoxelNet/train/{}.txt'.format(i), 'w')
    _3d_file.write(content_3d)
    _3d_file.close()
    

    print(i)


    

    

    

    


