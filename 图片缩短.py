import cv2
import os
import shutil

输入文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\train'
输出文件夹=r'D:\gitcangku\eggkid_mob_spawner\yolo-ui\datasets\bvn\images\train'

def resize_images_in_folder(input_folder, output_folder, scale_factor=2):
    """
    将输入文件夹中的所有图片缩放并保存到输出文件夹中。

    参数：
    - input_folder (str): 包含要缩放图片的文件夹路径。
    - output_folder (str): 将缩放后的图片保存到的文件夹路径。
    - scale_factor (int, 可选): 用于缩放图片的因子。默认为2。

    返回：
    None
    """
    # 创建输出文件夹如果它不存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Process all images in input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.jpg') or filename.endswith('.png'):
            # Read image
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # Resize image
            new_size = (img.shape[1] // scale_factor, img.shape[0] // scale_factor)
            resized_img = cv2.resize(img, new_size, interpolation=cv2.INTER_AREA)

            # Save resized image
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, resized_img)
            print(f'Resized {filename} and saved to {output_folder}')



if __name__ == '__main__':
    """"""
    resize_images_in_folder(输入文件夹, 输出文件夹, 缩短倍数=2)

