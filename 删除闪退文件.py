import os

file_path = r"C:\Users\11923\.labelImgSettings.pkl"

if os.path.exists(file_path):
    os.remove(file_path)
    print("文件已删除")
else:
    print("文件不存在")