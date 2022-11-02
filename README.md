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


### （2）将2D txt文件重命名

将./nuScenes_2d_tools/2D_label_parser/target_labels/CAM_FRONT/文件夹复制到 ./raw/2d_label/labels/CAM_FRONT/ 下

并将原数据集中的图片都拷到 ./nuScenes/raw/2d_label/imgs/CAM_FRONT 下

```
python rename.py
```

重命名后的所有文件保存在 ./new/2d_label/labels/CAM_FRONT/ 路径下

文件中每一行为： class xmin ymin xmax ymax

其中class包含 car pedestrian bicycle moveable_object 四类
