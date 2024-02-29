import numpy as np
import joblib
from config import RANDOM_FOREST_MODEL
import Controlers.GetLabeledData as get 


loaded_model = joblib.load(RANDOM_FOREST_MODEL)



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




class ToothClassifier:
    """
    Tooth shoould be [xywh_box]
    """
    def __init__(self,w,h,tooth):
        self.len=len(tooth)
        """ Number of tooth"""
        self.cls=[-1 for i in range(self.len)]
        """ Classes of tooth"""

        tw=[t[2] for t in tooth]
        sorted_tw=sorted(tw) # 大到小
        ranks_tw = {val: i/(self.len-1) for i, val in enumerate(sorted_tw)}# i:排名, val:原始值

        th=[t[3] for t in tooth]
        sorted_th = sorted(th)
        ranks_th = {val:i/(self.len-1) for i,val in enumerate(sorted_th)}




        self.features=[[ #from xywh
            t[0]/w,
            t[1]/h,
            t[2]/w,
            t[3]/h,
            w/h,
            ranks_tw[tw[i]],# Rank w
            ranks_th[th[i]] # Rank t

        ] for i,t in enumerate(tooth)]
        


        self.predicts=loaded_model.predict_proba(self.features)

        self.analysis()
        
        




    
    def analysis(self):
        
        self._now=self.predicts.copy()
        self._result=[[] for i in range(NUM_LABELS)]

        for i in range(self.len):
            self.add(i)

        self.cls=[-1 for i in range(self.len)]

        for i in range(len(self._result)):
            for t in self._result[i]:
                self.cls[t]=i

        

    
    def add(self,ti):


        cls=np.argmax(self._now[ti])

        if cls>6:
            print('class error')
            return
        
        self._result[cls].append(ti)
        if cls in (0,6) :
            return
        elif cls == 1 and len(self._result[1])<3:
            return
        elif cls in (2,3,4,5) and len(self._result[cls])<2:
            return
        
        
        member=np.array(self._result[cls])
        argpmin=np.argmin([self._now[t][cls] for t in member])
        pmin=member[argpmin]
        self._result[cls][argpmin]=self._result[cls][-1]
        self._result[cls].pop()

        adder=self._now[pmin][cls]
        self._now[pmin][cls]=0
        adder=adder/(sum([int(i>0) for i in self._now[pmin]])-1)
        for i in range(len(self._now[pmin])-1):
            if self._now[pmin][i+1]>0:
                self._now[pmin][i+1]+=adder

        #print(f'gg,{cls=},{pmin=},{result[cls]=}')
        #END+=1

        self.add(pmin)

    

    @staticmethod
    def get_feature_masks(img_path, masks):
        from Models.Polygon import Polygon 
        import cv2



        img=cv2.imread(img_path)
        h,w,d = img.shape
        result=[]


        l=len(masks)

        masks=[Polygon(m) for m in masks]

        mw=[m.bbox[2] for m in masks]
        sorted_mw=sorted(mw) # 大到小
        ranks_mw = {val: i/(l-1) for i, val in enumerate(sorted_mw)}# i:排名, val:原始值

        mh=[m.bbox[3] for m in masks]
        sorted_mh = sorted(mh)
        ranks_mh = {val:i/(l-1) for i,val in enumerate(sorted_mh)}




        features=[[
            m.center[0]/w,
            m.center[1]/h,
            m.bbox[2]/w,
            m.bbox[3]/h,
            w/h,
            ranks_mw[mw[i]],# Rank w
            ranks_mh[mh[i]] # Rank t

        ] for i,m in enumerate(masks)]




        return features


def BuildDataSet():
    input = get.get_all_data()
    x = []
    y = []
    

    for data in input:
        # Filter
        masks=[]
        for m,l in zip(data['mask'],data['label']):
            if str(l)=='-1':
                continue
            try:
                y.append(label_map[l])
            except:
                y.append(0)
            masks.append(m)



        features=ToothClassifier.get_feature_masks(data["path"], masks)

        for f in features:
            x.append(f)



    return x,y
