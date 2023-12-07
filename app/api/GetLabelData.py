from flask import Flask, request, Blueprint,jsonify,current_app
from lib.Base64Converter import url_to_img,path_to_base64
#from lib.SMILE import SMILE
import uuid
import numpy as np
from os import listdir,path,replace
import json
import random as rd
from PIL import Image
from pathlib import Path 
from datetime import datetime
#from flask_mail import Mail, Message

GetLabelData_blueprint= Blueprint('GetLabelData_blueprint', __name__)

@GetLabelData_blueprint.route('/get_label_data', methods=['POST','GET'])
def upload_img():
    
    if request.method== 'POST':
        try:
            return post(request.get_json())
        except:
            return "DataType error"

    elif request.method== 'GET':
        return get()

    


"""def add(data):
    #img_src=str(data.get('image'))
    img,ext=url_to_img(data.get('image'))
    id=uuid.uuid4()
    #filename = "upload_fig/{}.{}".format(id, ext)
    filename = "{}.{}".format('input', ext)

    with open(filename, "wb") as f:
        f.write(img)
    
    nowfig=SMILE(filename,'output' )
    #nowfig.set_predictor()
    nowfig.find_all_tooth()
    #mask,sc=nowfig.predict([[50,14]])

    return {'msg': 'success','filename':filename,"result":nowfig.base64, "score":100}
"""

def get():
    print(path.dirname(path.abspath(__file__)))
    #return {"fig":path.dirname(path.abspath(__file__))}
    

    dir_path=Path('.')/'app'/'TrainData'
    dir_path=str(dir_path.resolve())
    print("now",dir_path)

    
    files = listdir(dir_path+'/mask/')
    for f in files:
        size=''
        
        if f.split('.')[-1]=="png":
            with Image.open(f'{dir_path}/mask/{f}') as i:
                size=i.size
            id=f.split('/')[-1].split('.')[0]
            mask_path=f'{dir_path}/mask/{id}.json'
            with open(mask_path) as m:
                result={'mask':json.load(m)}
                result['fig']=path_to_base64(f'{dir_path}/mask/{f}')
                
                result['size']=size
                result['id']=id

                return result
    """except:
        return {'msg':'超出範圍'}"""

def post(jdata):
    print (jdata)
    id=jdata["id"]
    abs_path=path.dirname(path.abspath(__file__)).split('/')
    abs_path[-1]='TrainData'
    dir_path="/".join(abs_path)

    filename=datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    replace(f"{dir_path}/mask/{id}.png", f"{dir_path}/labeled/image/{filename}.png")

    with open(f"{dir_path}/labeled/mask/{filename}.json", "w") as f:
        json.dump(jdata, f)
    return "upload success!"
