import numpy as np
import cv2
import matplotlib.pyplot as plt
from os import listdir

from config import LABELED_IMAGE_DIR, LABELED_MASK_DIR

files = listdir(LABELED_IMAGE_DIR)


def show_sample():
    import random as rd
    import json
    image = rd.choice(files)
    mask_path = LABELED_MASK_DIR+image.split('.')[0]+'.json'

    print(LABELED_IMAGE_DIR+image)

    with open(mask_path) as f:
        mask=json.load(f)


    currentAxis = plt.gca()

    plt.imshow(plt.imread(LABELED_IMAGE_DIR+image))
    colors=plt.cm.hsv(np.linspace(0, 1, len(mask['label']))).tolist()
    #colors= rd.shuffle(colors)
    
    for m,l,c in zip(mask['mask'],mask['label'],colors):
        m=np.array(m)
        plt.plot(m[:,0],m[:,1],color=c)
        currentAxis.text(min(m[:,0]), min(m[:,1]), l,bbox={'facecolor': c, 'alpha': 0.5})
    
    plt.title(image)
    plt.show()
    return LABELED_IMAGE_DIR+image, mask['mask'], mask['label']


def get_sample():
    import random as rd
    import json
    image = rd.choice(files)
    mask_path = LABELED_MASK_DIR+image.split('.')[0]+'.json'

    with open(mask_path) as f:
        mask=json.load(f)


    return LABELED_IMAGE_DIR+image, mask['mask'], mask['label']


def get_all_data():
    import json
    result=[]


    for image in files:
    
        mask_path = LABELED_MASK_DIR+image.split('.')[0]+'.json'
        with open(mask_path) as f:
            mask=json.load(f)
        result.append({
            "path":LABELED_IMAGE_DIR+image,
            "mask":mask['mask'],
            "label":mask['label']
        })

    return result
