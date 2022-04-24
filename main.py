import requests 
import json

from flask import Flask
from flask_restful import Resource, Api, reqparse, request 

import os 
from dotenv import load_dotenv

import xml.etree.ElementTree as ET

app = Flask(__name__)
api = Api(app)

load_dotenv()
API_KEY = os.getenv("API_KEY")

@app.route("/speedlimit/<latitude>/<longitude>")
def speed_limit(latitude = "33.2545787", longitude = "-97.1532125"): 
    try: 
        url = "http://www.overpass-api.de/api/interpreter"
        body = { "data" : f"way(around:200,{latitude},{longitude})[maxspeed];out;"}
        r = requests.post(url, body) 
        root = ET.fromstring(r.text)
        speeds = root.findall(".//tag[@k='maxspeed']")
        max_speed = 0 
        for x in speeds: 
            max_speed = max(int(x.attrib['v'][:-4]), max_speed)
        return {'status': 'success', 'speedLimit': max_speed}
    except: 
        return {'status': 'failure'}

if __name__ == '__main__': 
    app.run()
    #print(speed_limit()) 

    

