




"""def get_feature_masks(img_path, masks):

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
"""
