import Controlers.GetLabeledData as get 
from Models.Polygon import Polygon 
import cv2

label=['11','21','12','22','13','23','14','24','15','25','16','26','17','27']
#label_now=[1,1,2,2,3,3,4,4,5,5,5,5,5,5]
label_now=[1,1,2,3,4,5,6,6,6,6,6,6,6,6]

label_map={ l:n for l,n in zip(label,label_now)}

ALL_LABELS=set(label_now)
NUM_LABELS=len(ALL_LABELS)+1
FDI_MAP={
    0:'L',
    1:'1',
    2:'12',
    3:'22',
    4:'13',
    5:'23',
    6:'pm/m'
}


def get_feature(img_path, masks):

    img=cv2.imread(img_path)
    h,w,d = img.shape
    result=[]

    for m in masks:
        m=Polygon(m)
        f=[
            m.center[0]/w,
            m.center[1]/h,
            m.bbox[2]/w,
            m.bbox[3]/h,
            w/h,
        ]

        result.append(f)

    return result




def BuildDataSet():
    input = get.get_all_data()
    x = []
    y = []
    

    for data in input:
        img=cv2.imread(data["path"])
        h,w,d = img.shape

        for l,m in zip(data['label'],data['mask']):
            if str(l)=='-1':
                continue
            m=Polygon(m)
            f=[
                m.center[0]/w,
                m.center[1]/h,
                m.bbox[2]/w,
                m.bbox[3]/h,
                w/h,
            ]

            x.append(f)
            try:
                y.append(label_map[l])
            except:
                y.append(0)
    return x,y
