
import numpy as np
import cv2
import matplotlib.pyplot as plt
import math



class Polygon:

    def __init__(self,arr):
        self.points=np.array(arr)
        
        self.n=len(self.points)
        """
        len(self.points)
        """
        
        self.area=self.count_area()
        try:
            self.box=[min(self.points[:,0]),max(self.points[:,0]),min(self.points[:,1]),max(self.points[:,1])]
            """
            [left,right,up,down]
            """

            self.bbox=[min(self.points[:,0]),min(self.points[:,1]),self.box[1]-self.box[0],self.box[3]-self.box[2]]
            """
            [left, up, width, height]
            """
            #lrud
            self.center=[np.mean(self.points[:,0]),np.mean(self.points[:,1])]
        except:
            print(self.points)
        self.width=self.bbox[2]
        self.height=self.bbox[3]

        
        pass
    def isin(self,pt):
        def interpolate_x(y,p1,p2):
            if (p1[1]==p2[1] or y==p1[1]):
                return p1[0]
            return p1[0] + (p2[0] - p1[0]) * (y - p1[1]) / (p2[1] - p1[1])
        
        c=False
        for i in range(self.n):
            p1=self.points[i-1]
            p2=self.points[i]
            if ((p1[1]-pt[1]>0)^(p2[1]-pt[1]>0)) and (pt[0]-p1[0])*(p2[1]-p1[1])-(pt[1]-p1[1])*(p2[0]-p1[0])==0 :
                #print(pt)
                return True
        
            
            if ((p1[1]-pt[1]>0)^(p2[1]-pt[1]>0)) and pt[0]<interpolate_x(pt[1], p1, p2):
                c=not c

        return c


        
        """return np.array([Polygon([pt,self.points[i],self.points[(i+1)%self.n]]).area*self.area>=0 for i in range(self.n)]).all()"""
    
    def count_area(self):
        if self.n<3:
            return 0
        area = 0
        q = self.points[-1]
        for p in self.points:
            area += p[0] * q[1] - p[1] * q[0]
            q = p
        return -area / 2

    def show(self):
        x=self.points[:,0]
        y=self.points[:,1]
        if (self.points[-1]!=self.points[0]).any():
            x=np.append(x,x[:1])
            y=np.append(y,y[:1])
        #mask=np.zeros(self, np.uint8)
        plt.figure(figsize=(10,10))
        plt.axis('on')
        plt.plot(x,y,'black')
        plt.fill(x,y, 'r')


        plt.show()
        #plt.fill(self.points[:,0],self.points[:,1],'b',alpha=0.5)
        pass
    def draw(self):
        x=self.points[:,0]
        y=self.points[:,1]
        if (self.points[-1]!=self.points[0]).any():
            x=np.append(x,x[:1])
            y=np.append(y,y[:1])
        #mask=np.zeros(self, np.uint8)
        plt.plot(x,y)
        #plt.fill(x,y, 'r')
        pass
    def expand(self,x):
        v1=[self.points[0][0]-self.points[-1][0],self.points[0][1]-self.points[-1][1]]
        l1=math.sqrt(v1[0]*v1[0]+v1[1]*v1[1])
        v2=[self.points[1][0]-self.points[0][0],self.points[1][1]-self.points[0][1]]
        l2=math.sqrt(v2[0]*v2[0]+v2[1]*v2[1])
        result=[]
        for i in range(self.n):
            q=[int(self.points[i][0]+x*(v1[0]/l1-v2[0]/l2)),int(self.points[i][1]+x*(v1[1]/l1-v2[1]/l2))]
            result.append(q)
            v1=v2
            l1=l2
            v2=[self.points[(i+2)%self.n][0]-self.points[(i+1)%self.n][0],self.points[(i+2)%self.n][1]-self.points[(i+1)%self.n][1]]
            l2=math.sqrt(v2[0]*v2[0]+v2[1]*v2[1])
        return Polygon(result)
    def gen_grid(self,l):
        result=[]
        #x,y=self.box[0],self.box[2]
        for x in np.arange(self.box[0], self.box[1], l[0]):
            for y in np.arange(self.box[2], self.box[3], l[1]):
                if self.isin([x,y]):
                    #print(self.isin([x,y]))
                    result.append([x,y])
        return np.array(result)
    def pol_to_mask(self):
            mask=np.zeros([1000,1000], np.uint8)
            #cv2.polylines(mask, np.int32([pol]), isClosed=True,color=1, thickness=1)
            try:
                cv2.fillPoly(mask,[self.points],1)
            except:
                print("can't fill",self.points)
            return mask
    
    @staticmethod
    def mask_to_pol(mask):
        mask=np.array(mask, dtype='uint8')

        contours, hierarchy = cv2.findContours(mask*255, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        try:
            pol=contours[0].reshape(-1,2) 
            return Polygon(pol)
        except:
            return []
        

class PolygonSet:
    def __init__(self):
        self.polygons=[]

    def append(self,pol):
        for e in self.polygons:
            if PolygonSet.isSame(e,pol):
                return
        self.polygons.append(pol)
        
    def clear(self):
        self.polygons=[]


    def isSame(pol1,pol2):
        
        pol1=Polygon(pol1)
        pol2=Polygon(pol2)
        if (pol1.center[0]-pol2.center[0])**2+(pol1.center[1]-pol2.center[1])**2>18:
            return False
        
    

        xor=(pol1.pol_to_mask()+pol2.pol_to_mask())%2
        #show_mask(xor)
        return sum(xor.flatten())/(abs(pol1.area)+abs(pol2.area))<0.2
    
    
    def show_mask(mask):
        w,h=mask.shape
        new=mask.reshape(h, w, 1)*1

        color = np.array([30/255, 144/255, 255/255, 0.6])
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        plt.gca().imshow(mask_image)
    
    
    
