from flask import Flask
from flask import request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
import uuid
from PIL import Image
import os
import operator
from werkzeug.datastructures import FileStorage
import numpy as np
from sklearn.cluster import KMeans
import time
import math

#Create API
app = Flask(__name__)
CORS(app)
api = Api(app)

def getHex(value):
    if(value < 16):
        return str(0) + hex(value).split('x', 1 )[1]
    return hex(value).split('x', 1 )[1]

def hexToRGB(h):
    rgb = []
    hex = h[0]
    rgb.append(int(hex[0:2], 16))
    rgb.append(int(hex[2:4], 16))
    rgb.append(int(hex[4:6], 16))
    return rgb

def generatePalette(img):
    palette = []
    colors = {}
    pixels = img.load()
    #Create Hex Dictionary of Occurences
    #Offest is the size of jump
    if(img.height > img.width):
        offset = int(math.ceil(img.height/500.0))
    else:
        offset = int(math.ceil(img.width/500.0))
    for x in range(0, img.width-(offset + 1), offset):
        for y in range(0, img.height-(offset + 1), offset):
            hexValue = (getHex((int(pixels[x,y][0] / 10)) * 10)) + (getHex((int(pixels[x,y][1] / 10)) * 10)) + (getHex((int(pixels[x,y][2] / 10)) * 10))
            if colors.get(hexValue) != None:
                colors[hexValue] = colors[hexValue] + 1
            else:
                colors[hexValue] = 1
    #Sort by number of occurecnes
    sortedColors = sorted(colors.items(), key=operator.itemgetter(1))
    #Get the top 10% of colors if there are more than 50 colors of colors
    if len(sortedColors) > 500:
        topColors = sortedColors[int(len(sortedColors)*0.99) : len(sortedColors)]
    #If there are less than 5 colors throw error
    elif(sortedColors < 5):
        return {"error": "not enough colors"}
    else:
        topColors = sortedColors


    tempA = []
    for i in range(0, len(topColors)):
        tempA.append(hexToRGB(topColors[i]))
    a = np.array(tempA)
    kmeans = KMeans(n_clusters=5)
    try:
        kmeans.fit(a)
    #If there are not enough colors to perform kmeans throw error
    except:
        return {"error": "not enough colors"}

    #Get centroids
    centroids = kmeans.cluster_centers_
    #Get Labels
    labels = kmeans.labels_
    palette = []
    #Format centroids into hex
    for i in range(0, 5):
        palette.append("#" + getHex(int(centroids[i][0])) + getHex(int(centroids[i][1])) + getHex(int(centroids[i][2])))
    return palette


class UploadImage(Resource):
    def post(self):
        #Generate uuid
        iid = uuid.uuid4().hex
        #Save file temporarilty 
        FileStorage(request.files['file']).save(str(iid))
        #Try to open image
        try:
            img = Image.open(iid)
        except: 
            #If image cant be open, throw error 
            os.remove(iid)
            return {"error": "not an Image"}
        # Get palette
        palette = generatePalette(img)
        #delete image
        os.remove(iid)
        #If error, return error
        if(type(palette) is dict):
            return palette
        #Return pallette
        else:
            return {"color1": palette[0], "color2": palette[1], "color3": palette[2], "color4": palette[3], "color5": palette[4]}
api.add_resource(UploadImage, '/upload')

if __name__ == '__main__':
    app.run(debug=True)

