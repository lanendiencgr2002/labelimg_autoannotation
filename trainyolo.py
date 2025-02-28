from ultralytics import YOLO
import os
def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)
切换到脚本所在目录()

datayaml=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\data.yaml'
pt='D:\gitcangku\eggkid_mob_spawner\yolo-ui\runs\detect\train7\weights\best.pt'

def 开始训练(datayaml="data.yaml",pt='yolov8n.pt'):
    '''
    开始训练
    Args:
        datayaml: 数据集路径
        pt: 模型路径
    '''
    from multiprocessing import freeze_support
    freeze_support()
    model = YOLO(pt)
    # batch：批次大小 16一般 条件可以的话32 条件差的8
    # epochs：训练轮数 小数据集30 大一些数据集50
    # imgsz：图片尺寸 像素小的320 像素大一些的640
    model.train(
        data=datayaml,
        workers=1,
        epochs=30,
        batch=16,
        imgsz=(320,320),
    )

if __name__ == '__main__':
    from multiprocessing import freeze_support
    freeze_support()
    # main()
    开始训练(datayaml=datayaml,pt=pt)

