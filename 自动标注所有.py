import os
import cv2
import numpy as np
from ultralytics import YOLO
from tqdm import tqdm

# 获取当前脚本的绝对路径
current_path = os.path.abspath(__file__)
# 获取脚本所在目录
script_dir = os.path.dirname(current_path)
# 切换到脚本所在目录
os.chdir(script_dir)
print('当前目录切换成功',script_dir)

图片所在目录=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\train'
标注文件所在目录=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\labels\train'
pt=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\runs\detect\train7\weights\best.pt'

class Model:
    def __init__(self, model_path=pt):
        self.model = YOLO(model_path)
        
    def detect(self, img_path):
        results = self.model(img_path)
        names = self.model.names
        cls = results[0].boxes.cls.cpu().numpy().astype(np.int32)
        obj_names = [names[i] for i in cls]
        xyxy = results[0].boxes.xyxy.cpu().numpy().astype(np.int32).tolist()
        conf = results[0].boxes.conf.cpu().numpy().tolist()
        objs = [
            {
                'cls': obj_names[id_],
                'xyxy': xyxy[id_],
                'conf': conf[id_]
            } for id_ in range(len(obj_names))
        ]
        return objs

def 读取classestxt文件(文件路径):
    '''
    在标注文件所在目录中查找classes.txt文件
    Args:
        文件路径: classes.txt文件所在目录路径
    Returns:
        list: 包含所有类别名称的列表
    '''
    classes_file = os.path.join(文件路径, 'classes.txt')
    if not os.path.exists(classes_file):
        raise FileNotFoundError(f'未找到classes.txt文件: {classes_file}')
        
    with open(classes_file, 'r', encoding='utf-8') as f:
        classes = [line.strip() for line in f.readlines()]
        
    return classes

def xyxy2yolo(box, img_width, img_height):
    '''
    将xyxy格式的边界框转换为YOLO格式(归一化的中心点坐标和宽高)
    '''
    x1, y1, x2, y2 = box
    
    # 计算中心点坐标
    cx = (x1 + x2) / 2 / img_width
    cy = (y1 + y2) / 2 / img_height
    
    # 计算宽高
    w = (x2 - x1) / img_width
    h = (y2 - y1) / img_height
    
    return [cx, cy, w, h]

def 自动标注(图片目录, 标注目录):
    '''
    对指定目录下的所有图片进行自动标注
    Args:
        图片目录: 图片所在目录路径
        标注目录: 标注文件保存目录路径
    '''
    # 确保标注目录存在
    if not os.path.exists(标注目录):
        os.makedirs(标注目录)
    
    # 读取类别列表
    classes = 读取classestxt文件(标注目录)
    class_dict = {name: i for i, name in enumerate(classes)}
    
    # 加载模型
    model = Model(pt)
    
    # 获取所有图片文件
    img_files = [f for f in os.listdir(图片目录) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    print(f'找到{len(img_files)}张图片,开始自动标注...')
    
    # 处理每张图片
    for img_file in tqdm(img_files):
        img_path = os.path.join(图片目录, img_file)
        
        # 读取图片获取尺寸
        img = cv2.imread(img_path)
        if img is None:
            print(f'无法读取图片: {img_path}')
            continue
            
        img_height, img_width = img.shape[:2]
        
        # 目标检测
        try:
            detections = model.detect(img_path)
        except Exception as e:
            print(f'处理图片时出错: {img_path}')
            print(f'错误信息: {str(e)}')
            continue
        
        # 生成标注文件名(与图片同名,但扩展名为.txt)
        label_file = os.path.join(标注目录, os.path.splitext(img_file)[0] + '.txt')
        
        # 写入标注文件
        with open(label_file, 'w', encoding='utf-8') as f:
            for det in detections:
                # 获取类别索引
                class_name = det['cls']
                if class_name not in class_dict:
                    print(f'未知类别: {class_name}')
                    continue
                class_idx = class_dict[class_name]
                
                # 转换边界框格式
                yolo_box = xyxy2yolo(det['xyxy'], img_width, img_height)
                
                # 写入一行: <class_idx> <x_center> <y_center> <width> <height>
                line = f"{class_idx} {' '.join([f'{x:.6f}' for x in yolo_box])}\n"
                f.write(line)
    
    print('自动标注完成!')

if __name__ == '__main__':
    自动标注(图片所在目录, 标注文件所在目录)


