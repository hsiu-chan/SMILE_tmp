from flask import Flask, request, Blueprint,jsonify,current_app
from lib.Base64Converter import url_to_img,path_to_base64
from lib.SMILE import SMILE
import uuid
import numpy as np

#from flask_mail import Mail, Message

img_blueprint = Blueprint('img_blueprint', __name__)

@img_blueprint.route('/upload_img', methods=['POST','GET'])
def upload_img():
    if request.method== 'POST':
        data=request.get_json()
        return add(data)
    elif request.method== 'GET':
        #x=data.get("xPos")
        #y=data.get("yPos")
        x,y=0,0
        return get(float(request.args.get('xPos')),float(request.args.get('yPos')))

    

"""@img_blueprint.route('/download_img', methods=['GET'])
def download_img():
    filename=request.get_json().get('filename')
    img_path=f'upload_fig/{filename}'
    base64_img = path_to_base64(img_path)  # base64编码
    return {'msg':'success',"base64_img":img_to_base64(img)}"""


def add(data):
    #img_src=str(data.get('image'))
    img,ext=url_to_img(data.get('image'))
    id=uuid.uuid4()
    #filename = "upload_fig/{}.{}".format(id, ext)
    filename = "{}.{}".format('input', ext)

    with open(filename, "wb") as f:
        f.write(img)
    
    nowfig=SMILE(filename,'output' )
    nowfig.set_predictor()
    nowfig.find_all_tooth()
    #mask,sc=nowfig.predict([[50,14]])

    return {'msg': 'success','filename':filename,"result":nowfig.base64, "score":100}


def get(x,y):
    #try:
    pol,sc=SMILE.predict(x,y)
    xpol=','.join([str(i) for i in pol[:,0]])
    ypol=','.join([str(i) for i in pol[:,1]])
    return {'xpol':xpol, 'ypol':ypol,'sc':sc, 'msg':'success'}
    """except:
        return {'msg':'超出範圍'}"""
