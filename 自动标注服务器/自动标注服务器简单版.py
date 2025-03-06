from dataclasses import dataclass
from pathlib import Path
import base64
import json
import cv2
import numpy as np
from flask import Flask, request, jsonify
from ultralytics import YOLO

# 配置
@dataclass
class Config:
    MODEL_PATH: str = './last.pt'
    DEFAULT_MODEL: str = './yolov8n.pt'
    HOST: str = '0.0.0.0' 
    PORT: int = 22234

# 初始化
Path(__file__).parent.absolute().chdir()
app = Flask(__name__)
model = YOLO(Config.MODEL_PATH)

def decode_image(image_base64: str) -> np.ndarray:
    """解码base64图像"""
    image_bytes = base64.b64decode(image_base64)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    return cv2.imdecode(image_array, cv2.IMREAD_COLOR)

def detect(image: np.ndarray) -> list:
    """目标检测"""
    results = model(image)[0]
    return [{
        'cls': model.names[int(cls)],
        'xyxy': box.tolist(),
        'conf': conf
    } for cls, box, conf in zip(
        results.boxes.cls.cpu().numpy(),
        results.boxes.xyxy.cpu().numpy(),
        results.boxes.conf.cpu().numpy()
    )]

@app.route('/recognize', methods=['POST'])
def recognize():
    """处理识别请求"""
    if not request.json or 'image' not in request.json:
        return jsonify({'error': 'No image data provided'}), 400
        
    image = decode_image(json.loads(request.json)['image'])
    return jsonify({'result': detect(image)})

if __name__ == '__main__':
    app.run(host=Config.HOST, port=Config.PORT)
