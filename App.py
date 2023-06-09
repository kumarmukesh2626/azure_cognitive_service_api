#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 13:02:36 2022

@author: Mukesh, Arresh
"""

'''
API based approach to run models on images.
    Developer: Mukesh
    Company: Algo8AI
    Date: 20-Nov-2022
'''
from PIL import Image
import numpy as np
import io
# from waitress import serve
from flask_cors import CORS
from flask import Flask, jsonify, request
import time
import cv2
import configparser
import base64
import requests
from logs.config import success_log, error_log

config_Url = configparser.ConfigParser()
config_Url.read("config/common_config.ini")
test_batch_url = config_Url["configuration"]["test_batch_url"]

def stringToRGB(base64_string):
    try:
        imgdata = base64.b64decode(str(base64_string))
        img = Image.open(io.BytesIO(imgdata))
        opencv_img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        return (True, opencv_img)
    except:
        return (False, "not able to retrieve image")


def imageToBase64String(img):
    _, buffer = cv2.imencode('.jpg', img)
    return str(base64.b64encode(buffer).decode('utf-8'))


#  creating flask app to host the api's at
app = Flask(__name__)
# cors initialization so that all modern browsers can identify as url (*not required for API development*)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# post api which accepts inputs as follows


import json
import requests

@app.route('/api/v1/objectdetection', methods=['POST'])
def batch_automation():
    try:
        success_log("POST method call successful", "201", "main.automation")
        start = time.time()
        # read json data send via api
        success_log("reading json data from api", "202", "__main__")
        batch_data = request.json
        batch_out_json = []
        #  fetching both camid and frame
        for img_data in batch_data:
            frame = img_data["frame"]
            camid = img_data['camid']
            print(camid)
            # converting base64 frame to cv2 image so that it can be used via YOLOv5 model
            t = time.time()
            assert subscription_key
            headers = {'Content-Type': 'application/octet-stream', 'Prediction-Key': subscription_key}
            status, original_frame = stringToRGB(frame)
            _, buffer = cv2.imencode('.jpg', original_frame)
            print("Sending Response to Azure Cognitive Service API")
            response = requests.post(endpoint, headers=headers, data=buffer.tobytes())
            print("response",response)
            print(response.text)
            b64_time = time.time()     
            b64_end_time = time.time()
            success_log("time taken to convert frame" + str(b64_end_time - b64_time), "205", "automation")
            success_log("total time taken for current instances" + str(b64_end_time - start), "205", "automation")

            # running model
            t1 = time.time()
            t1_model = time.time()  
            success_log("completion of process in yolov5 model" + str(t1_model - t1), "205", "automation")
            frames = imageToBase64String(original_frame)
            #  fetching data in correct json format
            batch_out_json.append({
                "Status": True,
                "Message": "All process success",
                "Results": json.loads(response.text),  # Convert response data to Python dictionary
                "camid": camid,
                "frame": frames
            })
            success_log("Model response recorded.", "204", "__main__.automation")
            end = time.time()
            success_log("Time taken to generate and send response :{}".format(end - start), "205", "automation")
        
        #  send positive response to the client
        return jsonify(batch_out_json), 200
    except Exception as error:
        print(error)
        error_log("Flask api initalization failed.", "500", "__main__")        

if __name__ == '__main__':
    success_log("initialising flask api.", "101", "__main__")
    # calling config parameters in the code 
    try:
        try:
            config_value = configparser.ConfigParser()
            config_value.read('config/common_config.ini')
            model_dir = config_value["model"]["model_dir"]
            weights = config_value["model"]["weights"]
            subscription_key = config_value['azure_services']['subscription_key']
            project_id = config_value['azure_services']['project_id']
            published_name = config_value['azure_services']['published_name']
            endpoint = config_value['azure_services']['api_endpoint']
            conf = float(config_value['configuration']['confidence'])
            success_log("Config values for model picked up.", "102", "__main__")
        except:
            error_log("Not able to fetch config file/values.", "500", "__main__")
        success_log("Initalizing YOLOv5 model", "103", "__main__")
        #  run server based on values in config file
        if config_value["API"]["API_instance"] == "PROD":
            success_log("running API in production mode.", "200", "__main__")
            print("API Is Running")
            app.run(host="0.0.0.0")
            
        elif config_value["API"]["API_instance"] == "DEBUG":
            success_log("running API in development mode", "200", "__main__")
            app.run(host="0.0.0.0")
        else:
            success_log("running API in testing mode. debug is off.", "200", "__main__")
            app.run(host="0.0.0.0")
    except Exception as e:
        print(e)
        error_log("Flask api initalization failed.", "500", "__main__")



