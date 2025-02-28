# 用于清空训练集和标签等
import os
import shutil
训练集文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\train'
训练集标签文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\labels\train'
验证集文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\val'
验证集标签文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\labels\val'

def 清空文件夹(文件夹路径):
    """
    清空指定文件夹下的所有内容,包括文件、子文件夹和符号链接
    
    参数:
        文件夹路径: 要清空的文件夹路径
    """
    if not os.path.exists(文件夹路径):
        print(f"文件夹 {文件夹路径} 不存在")
        return
        
    for 项目 in os.listdir(文件夹路径):
        项目路径 = os.path.join(文件夹路径, 项目)
        try:
            if os.path.isfile(项目路径) or os.path.islink(项目路径):
                os.unlink(项目路径)  # 删除文件或符号链接
                print(f"已删除文件: {项目路径}")
            elif os.path.isdir(项目路径):
                shutil.rmtree(项目路径)  # 删除文件夹及其所有内容
                print(f"已删除文件夹: {项目路径}")
        except Exception as e:
            print(f"删除 {项目路径} 失败,原因: {e}")
            
    print(f"文件夹 {文件夹路径} 已清空")
def 清空文件夹保留classestxt文件(文件夹路径):
    '''
    清空文件夹保留classestxt文件
    '''
    if not os.path.exists(文件夹路径):
        print(f"文件夹 {文件夹路径} 不存在")
        return
        
    for 项目 in os.listdir(文件夹路径):
        if 项目 == "classes.txt":  # 跳过classes.txt文件
            continue
            
        项目路径 = os.path.join(文件夹路径, 项目)
        try:
            if os.path.isfile(项目路径) or os.path.islink(项目路径):
                os.unlink(项目路径)  # 删除文件或符号链接
                print(f"已删除文件: {项目路径}")
            elif os.path.isdir(项目路径):
                shutil.rmtree(项目路径)  # 删除文件夹及其所有内容
                print(f"已删除文件夹: {项目路径}")
        except Exception as e:
            print(f"删除 {项目路径} 失败,原因: {e}")
            
    print(f"文件夹 {文件夹路径} 已清空(保留classes.txt)")
def 清空训练集所有数据():
    '''
    清空训练集所有数据
    '''
    清空文件夹(训练集文件夹)
    清空文件夹(训练集标签文件夹)
def 清空训练集所有数据保留classestxt文件():
    '''
    清空训练集所有数据保留classestxt文件
    '''
    清空文件夹保留classestxt文件(训练集文件夹)
    清空文件夹保留classestxt文件(训练集标签文件夹)
def 清空验证集所有数据():
    '''
    清空验证集所有数据
    '''
    清空文件夹(验证集文件夹)
    清空文件夹(验证集标签文件夹)
def 清空验证集所有数据保留classestxt文件():
    '''
    清空验证集所有数据保留classestxt文件
    '''
    清空文件夹保留classestxt文件(验证集文件夹)
    清空文件夹保留classestxt文件(验证集标签文件夹)

if __name__ == "__main__":
    清空训练集所有数据保留classestxt文件()

