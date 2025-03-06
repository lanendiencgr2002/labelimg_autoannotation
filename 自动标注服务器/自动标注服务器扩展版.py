import base64
import json
import logging
from datetime import datetime
import cv2
from ultralytics import YOLO
import numpy as np
from flask import Flask, request, jsonify
from logging.handlers import RotatingFileHandler
import os
import random
def 切换到脚本所在目录():
    # 获取当前脚本的绝对路径
    current_path = os.path.abspath(__file__)
    # 获取脚本所在目录
    script_dir = os.path.dirname(current_path)
    # 切换到脚本所在目录
    os.chdir(script_dir)
    print('当前目录切换成功',script_dir)
切换到脚本所在目录()




pt=r'D:\gitcangku\eggkid_mob_spawner\pt\baobaohu_newestpt\best.pt'
def setup_logger():
    # 创建logs目录
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 设置日志文件名(使用当前日期)
    log_file = f'logs/server_{datetime.now().strftime("%Y%m%d")}.log'
    
    # 创建logger
    logger = logging.getLogger('server_logger')
    logger.setLevel(logging.INFO)
    
    # 创建RotatingFileHandler
    # maxBytes=10*1024*1024 表示10MB
    # backupCount=5 表示保留5个备份文件
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    
    # 设置日志格式
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    # 添加处理器到logger
    logger.addHandler(file_handler)
    
    return logger

# 创建logger实例
logger = setup_logger()
app = Flask(__name__)
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
model = Model(pt)

@app.route('/recognize', methods=['POST'])
def recognize():
    if not request.json or 'image' not in request.json:
        logger.error('No image data provided')
        return jsonify({'error': 'No image data provided'}), 400
    
    try:
        image_base64 = json.loads(request.json)['image']
        logger.info("接收到图像数据请求")
        
        image_bytes = base64.b64decode(image_base64)
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        # 放图片
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        random_num = random.randint(1000, 9999)
        
        cv2.imwrite(f'./服务器接收的截图/{timestamp}_{random_num}.png', image)

        result = model.detect(image)
        
        # 检查是否需要保存图片
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        save_dir = os.path.join('logs', 'low_conf_images', datetime.now().strftime("%Y%m%d"))
        os.makedirs(save_dir, exist_ok=True)
        
        if not result:  # 没有检测到目标
            save_path = os.path.join(save_dir, f'未检测_{timestamp}.jpg')
            cv2.imwrite(save_path, image)
            logger.warning(f"未检测到目标,图片已保存: {save_path}")
        else:
            # 检查是否有低置信度的检测
            min_conf = min(obj['conf'] for obj in result)
            if min_conf < 0.9:
                # 找到置信度最低的目标的类别
                min_conf_obj = min(result, key=lambda x: x['conf'])
                conf_int = int(min_conf_obj['conf'] * 100)
                save_path = os.path.join(save_dir, f'{min_conf_obj["cls"]}_{conf_int}_{timestamp}.jpg')
                cv2.imwrite(save_path, image)
                logger.warning(f"检测到低置信度目标,图片已保存: {save_path}")
        
        # 格式化检测结果为简洁的字符串
        detections = [f"{obj['cls']}({obj['conf']:.2f})" for obj in result]
        logger.info(f"检测完成: {', '.join(detections)}")
        
        return jsonify({'result': result})
        
    except Exception as e:
        logger.error(f"处理请求时发生错误: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/shutdown', methods=['POST'])
def shutdown():
    logger.info("收到关闭服务器请求")
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        logger.error("Not running with the Werkzeug Server")
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    logger.info("服务器正在关闭...")
    return 'Server shutting down...'

if __name__ == '__main__':
    logger.info("服务器启动...")
    app.run(host='0.0.0.0',port=22234)  # 在调试模式下运行，方便调试
    
