import requests 

from flask import Flask
from flask_restful import Resource, Api, reqparse, request 

import os 
from dotenv import load_dotenv

import xml.etree.ElementTree as ET

app = Flask(__name__)
api = Api(app)

load_dotenv()
API_KEY = os.getenv("API_KEY")

# deprecated google maps API 
# @app.route("/get_speed_limit")
# def speed_limit(latitudes = [], longitudes = []): 
#     key = 'AIzaSyB3MhdUlM3OuRg218wsWZjwRPkPUd9mWC4'
#     if not latitudes or not longitudes: 
#         path = '38.75807927603043,-9.03741754643809|38.6896537,-9.1770515|41.1399289,-8.6094075' 
#     else: 
#         path = ""
#     #print('https://roads.googleapis.com/v1/speedLimits?path={path}&key={API_KEY}')
#     #r = requests.get('https://roads.googleapis.com/v1/speedLimits?path={path}&key={API_KEY}') 
#     r = requests.get(f'https://roads.googleapis.com/v1/speedLimits?path={path}&key={key}') 
#     #r = requests.get('https://roads.googleapis.com/v1/speedLimits?path={path}&key=AIzaSyB3MhdUlM3OuRg218wsWZjwRPkPUd9mWC4') 
#     return r.text 

@app.route("/speedlimit/<latitude>/<longitude>")
def speed_limit(latitude = "33.2545787", longitude = "-97.1532125"): 
    url = "http://www.overpass-api.de/api/interpreter"
    body = { "data" : f"way(around:200,{latitude},{longitude})[maxspeed];out;"}
    r = requests.post(url, body) 
    root = ET.fromstring(r.text)
    speeds = root.findall(".//tag[@k='maxspeed']")
    max_speed = 0 
    for x in speeds: 
        max_speed = max(int(x.attrib['v'][:-4]), max_speed)
    return max_speed 
    

if __name__ == '__main__': 
    print(speed_limit()) 

    

