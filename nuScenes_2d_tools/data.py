# -*- coding: utf-8 -*-
import xml.dom.minidom
import os
root_path = '/home/thinking/detection_ws/nuScenes_tools/'
annotation_path = root_path + 'TXT/'
img_path = root_path + 'CAM_ALL/'
annotation_list = os.listdir(annotation_path)
img_list = os.listdir(img_path)
if len(img_list) != len(annotation_list):
    print("图片和标签数目不匹配")
    if len(img_list) < len(annotation_list):
        print("标签比图片多")
        error_xml = []
        for _ in annotation_list:
            xml_name = _.split('.')[0]
            img_name = xml_name + '.jpg'
            if img_name not in img_list:
                error_xml.append(_)
                # os.remove(_)
        print("error xml:", error_xml)
    
    else:
        print("图片比标签多")
        error_img = []
        for _ in img_list:
            img_name = _.split('.')[0]
            xml_name = img_name + '.txt'
            if xml_name not in annotation_list:
                error_img.append(_)
                print(_)
                # os.remove(_)
        # print("缺少标签的图片:", error_img)
