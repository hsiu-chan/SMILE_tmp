import os 
from pathlib import Path, PurePath

ROOT_PATH=os.path.dirname(os.path.abspath(__file__))+'/'
OUTPUT_DIR=ROOT_PATH+'output/'

# 標註
LABELED_DIR=ROOT_PATH+'app/TrainData/labeled/'
LABELED_IMAGE_DIR=LABELED_DIR+'image/'
LABELED_MASK_DIR=LABELED_DIR+'mask/'


# YOLO
YOLO_DATASET=ROOT_PATH+'YOLOv8/YOLOdataset/'
YOLO_BEST_PT=ROOT_PATH+'Assets/best.pt'
YOLO_V8M=ROOT_PATH+'YOLOv8/yolov8m.pt'
YOLO_V8N=ROOT_PATH+'YOLOv8/yolov8n.pt'


# Testing
TEST_IMG=ROOT_PATH+'Document/test.png'
RANDOM_FOREST_MODEL=ROOT_PATH+'Assets/random_forest_model.joblib'

# 隨機森林分類器
