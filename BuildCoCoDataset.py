from app.lib.Polygon import Polygon
import json
import numpy as np
import cv2
import os
import sys
import io
from pathlib import Path
import random as rd

if sys.version_info[0] >= 3:
    unicode = str
# __author__ = 'hcaesar'

# 实例的id，每个图像有多个物体每个物体的唯一id
global segmentation_id
segmentation_id = 0
Dir_path='./app/TrainData/labeled/' 

# 原图像的路径， 原图像和mask图像的名称是一致的。
path = Dir_path+'image/'
rgb_image_files = os.listdir(path)
# mask路径
block_mask_path = Dir_path+'mask/'
block_mask_files = os.listdir(block_mask_path)

# coco json保存的位置
jsonPath_t = Dir_path+"train.json"
jsonPath_v = Dir_path+"test.json"

with io.open(Dir_path+'cate.json') as f:
    a=json.load(f)
    cate={a[i]:i for i in range(len(a))}


# annotations部分的实现
def polyToanno(polygon_mask,category_id, image_id):
    annotations = [] #一幅图片所有的annotatons
    global segmentation_id
    # print(ann_count)
    # 对每个实例进行处理
    for i in range(len(polygon_mask)):
        if category_id[i]==-1:
            continue
        
        polygon=Polygon(polygon_mask[i])
        
        annotation = {
            "segmentation": [],
            "area": abs(polygon.area),
            "iscrowd": 0,
            "image_id": image_id,
            "bbox": polygon.bbox,
            "category_id": category_id[i],
            "id": segmentation_id
        }
        # print(contour)
        # 求segmentation部分
        segmentation = polygon.points.ravel().tolist()
        if len(segmentation)<=4:
            continue
        annotation["segmentation"].append(segmentation)
        annotations.append(annotation)
        segmentation_id = segmentation_id + 1
    return annotations

class NumpyEncoder(json.JSONEncoder):
    """ Custom encoder for numpy data types """
    def default(self, obj):
        if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                            np.int16, np.int32, np.int64, np.uint8,
                            np.uint16, np.uint32, np.uint64)):

            return int(obj)

        elif isinstance(obj, (np.float_, np.float16, np.float32, np.float64)):
            return float(obj)

        elif isinstance(obj, (np.complex_, np.complex64, np.complex128)):
            return {'real': obj.real, 'imag': obj.imag}

        elif isinstance(obj, (np.ndarray,)):
            return obj.tolist()

        elif isinstance(obj, (np.bool_)):
            return bool(obj)

        elif isinstance(obj, (np.void)): 
            return None

        return json.JSONEncoder.default(self, obj)

def build(jsonPath,arr):
    annCount = 0
    imageCount = 0

    file_dict={}

    with io.open(jsonPath, 'w', encoding='utf8') as output:
        # 那就全部写在一个文件夹好了
        # 先写images的信息
        output.write(unicode('{\n'))
        output.write(unicode('"images": [\n'))

        
        
        for image in arr:
            file_dict[image.split('.')[0]]=imageCount
            
            pic=cv2.imread(path+image)
            h,w,d=pic.shape

            output.write(unicode('{'))
            annotation = {
                "height": h,
                "width": w,
                "id": imageCount,
                "file_name": image
            }

            str_ = json.dumps(annotation, indent=4)
            str_ = str_[1:-1]
            if len(str_) > 0:
                output.write(unicode(str_))
                imageCount = imageCount + 1
            if (image == arr[-1]):
                output.write(unicode('}\n'))
            else:
                output.write(unicode('},\n'))
        output.write(unicode('],\n'))
        

        
        ################ 写cate ###############
        output.write(unicode('"categories": [\n'))

        for c in cate:
            output.write(unicode('{\n'))
            categories = {
                "supercategory": c,
                "id": cate[c],
                "name": c
            }
            str_ = json.dumps(categories, indent=4)
            str_ = str_[1:-1]
            if len(str_) > 0:
                output.write(unicode(str_))
            if c==list(cate)[-1]:
                output.write(unicode('}\n'))
            else:
                output.write(unicode('},\n'))

        output.write(unicode('],\n'))

        
        
        ############### 写annotations ###############
        output.write(unicode('"annotations": [\n'))
        for i in range(len(arr)):       
            
            with open(os.path.join(block_mask_path, f"{arr[i].split('.')[0]}.json")) as f:
                data=json.load(f)
            
            #label 轉換
            labels=[]
            for label in data['label']:
                try:
                    labels.append(cate[label])
                except:
                    labels.append(-1)


            #annotations
            block_anno = polyToanno(data['mask'],labels, file_dict[arr[i].split('.')[0]])
            
            
            for b in block_anno:
                #print (b)
                str_block = json.dumps(b, indent=4,cls=NumpyEncoder)
                str_block = str_block[1:-1]
                if len(str_block) > 0:
                    output.write(unicode('{\n'))
                    output.write(unicode(str_block))
                    if ( b == block_anno[-1] and i==len(arr)-1):
                        output.write(unicode('}\n'))
                    else:
                        output.write(unicode('},\n'))
            annCount = annCount + 1
        output.write(unicode(']\n'))
        output.write(unicode('}\n'))

def BuildCoCoDataset(k):
    

    
    rd.shuffle(rgb_image_files)

    idx=int(len(rgb_image_files)*k)
    
    
    
    print(f'build({jsonPath_t},{rgb_image_files[:idx]})')
    build(jsonPath_t,rgb_image_files[:idx])
    build(jsonPath_v,rgb_image_files[idx:])
