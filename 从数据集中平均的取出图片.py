# D:\gitcangku\eggkid_mob_spawner\图片集\baobaohu
# D:\gitcangku\eggkid_mob_spawner\图片集\dibengbeng
# D:\gitcangku\eggkid_mob_spawner\图片集\jiaohuogu
# D:\gitcangku\eggkid_mob_spawner\图片集\zhamaotuo
# D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\train

import os
import random
import shutil

# 目录应该是这样 大文件夹下 包含小文件夹 小文件夹下 包含图片   
# 例子：大文件夹->{文件夹1,文件夹2,文件夹3}
# 文件夹1->{图片*n}
# 文件夹2->{图片*n}
# 文件夹3->{图片*n}

大文件夹目录=r'D:\gitcangku\eggkid_mob_spawner\图片集'
训练集文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\train'
验证集文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\val'

def 从数据集中平均的取出图片(目标文件夹, 每个文件夹取的张数=50, 是否复制=False):
    """从数据集中随机取出指定数量的图片,可以选择移动或复制到目标文件夹。

    Args:
        目标文件夹 (str): 图片将被移动/复制到的目标文件夹路径
        每个文件夹取的张数 (int, optional): 从每个子文件夹中随机取出的图片数量. Defaults to 50.
        是否复制 (bool, optional): True表示复制文件,False表示移动文件. Defaults to False.
    Examples:
        >>> # 移动50张图片到训练集
        >>> 从数据集中平均的取出图片(训练集文件夹, 每个文件夹取的张数=50, 是否复制=False)
        >>> # 复制50张图片到验证集
        >>> 从数据集中平均的取出图片(验证集文件夹, 每个文件夹取的张数=50, 是否复制=True)
    Notes:
        - 源文件夹结构必须是: 大文件夹/子文件夹/图片文件
        - 如果子文件夹中的图片数量不足,会打印警告并使用所有可用的图片
        - 支持的图片格式: .png, .jpg, .jpeg
    """
    # 获取所有子文件夹
    子文件夹列表 = [os.path.join(大文件夹目录, d) for d in os.listdir(大文件夹目录) 
                if os.path.isdir(os.path.join(大文件夹目录, d))]

    # 确保目标文件夹存在
    os.makedirs(目标文件夹, exist_ok=True)
    
    total_count = 0
    操作方式 = "复制" if 是否复制 else "移动"
    
    # 从每个源文件夹处理指定张数的图片
    for source_dir in 子文件夹列表:
        # 获取源文件夹中的所有图片文件
        image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # 如果图片数量不足,打印警告
        if len(image_files) < 每个文件夹取的张数:
            print(f"警告: {source_dir} 中的图片少于{每个文件夹取的张数}张")
            num_to_process = len(image_files)
        else:
            num_to_process = 每个文件夹取的张数
        
        # 随机选择图片
        selected_images = random.sample(image_files, num_to_process)
        
        # 处理选中的图片
        for image in selected_images:
            source_path = os.path.join(source_dir, image)
            target_path = os.path.join(目标文件夹, image)
            if 是否复制:
                shutil.copy(source_path, target_path)
            else:
                shutil.move(source_path, target_path)
            print(f"已{操作方式}: {image}")
            total_count += 1

    print(f"完成! 总共{操作方式}了{total_count}张图片到目标目录。")


def 从数据集中随机取出图片(目标文件夹, 每个文件夹取的张数=50, 是否复制=False):
   

if __name__ == "__main__":
    # 移动图片到训练集
    从数据集中平均的取出图片(训练集文件夹, 每个文件夹取的张数=50, 是否复制=False)
    # 复制图片到验证集
    # 从数据集中平均的取出图片(验证集文件夹, 每个文件夹取的张数=50, 是否复制=True)
