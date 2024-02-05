from Polygon import Polygon
import json
import numpy as np
import cv2
import os
import sys
import io
import random as rd
import matplotlib.pyplot as plt
import shutil


if sys.version_info[0] >= 3:
    unicode = str
# __author__ = 'hcaesar'

#原標註路徑
Dir_path='../app/TrainData/labeled/' 

# 原圖的路径
image_dir = Dir_path+'image/'
rgb_image_files = os.listdir(image_dir)

# mask路径
block_mask_path = Dir_path+'mask/'
block_mask_files = os.listdir(block_mask_path)

# out put path 
Out_path = 'YOLOdataset/'



def build(path,arr):
    ### 清空 path
    try:
        shutil.rmtree(path)
    except OSError as e:
        print("Error: %s : %s" % (path, e.strerror))
    
    ### 重建 path
    os.makedirs(path+'images/')
    os.makedirs(path+'labels/')
    
    for filename in arr:
        name= filename.split('.')[0] # 檔名
        image_path=image_dir+filename
        mask_path = block_mask_path+name+'.json'

        
       

        # 讀入圖片
        fig= cv2.imread(image_path)
        h,w,d=fig.shape
        #plt.imshow(fig)

        shutil.copy(image_path, path+'images/')# 複製圖片

        #讀入mask
        with open(mask_path) as f:
            masks= json.load(f)
        #print(masks['label'])



        #寫 txt
        label_path=f"{path}labels/{name}.txt"
        with open(label_path,"w") as f:
            for i in range(len(masks['label'])):
                if int(masks['label'][i])==-1:
                    continue
                elif int(masks['label'][i]) in (13, 23):
                    cls=1
                elif int(masks['label'][i])/10 <3:
                    cls=0
                elif int(masks['label'][i])/10 >=3:
                    cls=2
                print(masks['label'][i], cls )


                    


                mask=Polygon(masks["mask"][i])
                
                width=mask.width
                height=mask.height
                cx=mask.bbox[0]+width/2
                cy=mask.bbox[1]+height/2

                f.write(f'{cls} {cx/w} {cy/h} {width/w} {height/h}\n')

                #####test
                #plt.text(cx, cy, masks['label'][i])
                #plt.scatter(cx,cy)
                #plt.gca().add_patch( plt.Rectangle((mask.bbox[0],mask.bbox[1]),width,height,fill=False,edgecolor='r',linewidth=2))
               


        #plt.show()

        #break

    

def BuildYOLODataset(k):
    

    
    rd.shuffle(rgb_image_files)

    idx=int(len(rgb_image_files)*k)
    
    
    
    print(f'build({Out_path},{rgb_image_files[:idx]})')
    build(Out_path+"train/",rgb_image_files[:idx])
    build(Out_path+"val/",rgb_image_files[idx:])
