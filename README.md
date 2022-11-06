# nuscenes-tools

## 1. 2D labels

### (1) 将2D json文件 转换为 2D txt文件

确保 ./nuScenes_2d_tools/2D_label_parser/target_labels/ 路径下包含六个相机文件夹，且文件夹内为空

```
cd ./nuScenes_2d_tools/2D_label_parser
python label_parser.py -dt nuscenes
```

运行可能会出错，但不用管

得到 ./nuScenes_2d_tools/2D_label_parser/target_labels/CAM_FRONT/ 下名字带时间戳的txt文件

详情可参考 https://blog.csdn.net/qq_34972053/article/details/111315493


### （2） 将2D txt文件重命名

将./nuScenes_2d_tools/2D_label_parser/target_labels/CAM_FRONT/文件夹复制到 ./raw/2d_label/labels/CAM_FRONT/ 下

并将原数据集中的图片都拷到 ./nuScenes/raw/2d_label/imgs/CAM_FRONT 下

```
python rename.py
```

重命名后的所有文件保存在 ./new/2d_label/labels/CAM_FRONT/ 路径下

文件中每一行为： class xmin ymin xmax ymax

其中class包含 car pedestrian bicycle moveable_object 四类

## 2. 3D detections

### (1) 3D txt文件获取
```
python rename.py
```

文件保存在 ./new/3d_detection/VoxelNet/train/ 路径下

每一行为 class x y z w l h yaw score

### （2） 3D txt文件类别重命名

```
python change_clss.py
```
文件保存在 ./new/3d_detection/VoxelNet/new/ 路径下

每一行为 class x y z w l h yaw score

其中class包含 car pedestrian bicycle moveable_object 四类

### (3) 3D detection评估

```
python select_from_json.py
```

生成mini-VoxelNet.json文件

而后

```
cd nuScenes_2d_tools/nuscenes-devkit/python-sdk/nuscenes/eval/detection/
python evaluate.py --version v1.0-mini --result_path /home/thinking/detection_ws/dataset/nuScenes/mini-VoxelNet.json
```
