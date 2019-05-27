from flask import Flask, render_template, Response
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import os
from flask import request, redirect, url_for
from werkzeug.utils import secure_filename
from cartooning import cartoon
from seuillage import adaptativeThreshold
from image_description import analyser_image
import cv2

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Encode les images en base64
def encode(file):
    byte_io = BytesIO()
    byte_io.write(file.read())
    byte_io.seek(0)
    figdata_png = base64.b64encode(byte_io.getvalue()).decode('ascii')
    return figdata_png

app = Flask(__name__)

camera = cv2.VideoCapture(0)  # use 0 for web camera

def gen_frames(filtre):  # generate frame by frame from camera
    sobelx=False
    sobely=False
    laplacien=False
    canny=False

    if filtre== "sobelx":
        sobelx = True
    if filtre== "sobely":
        sobely = True
    if filtre== "laplacien":
        laplacien = True
    if filtre== "canny":
        canny = True
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if sobelx==True:
            frame = cv2.Sobel(frame,cv2.CV_64F,1,0,ksize=5)
        if sobely==True:
            frame = cv2.Sobel(frame,cv2.CV_64F,0,1,ksize=5)
        if laplacien==True:
            frame = cv2.cv2.Laplacian(frame,cv2.CV_64F)
        if canny==True:
            frame = cv2.Canny(frame, 100, 200)
        
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

@app.route('/')
def hello_world():
    return render_template('index_1.html')#, result=figdata_png)

@app.route('/cartoon', methods=['GET', 'POST'])
def upload_cartoon_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            figdata_png = encode(file)
            figdata_png = cartoon(figdata_png)
            figdata_png = base64.b64encode(figdata_png).decode('ascii')
            return render_template('index_1.html' ,result=figdata_png)
@app.route('/threshold', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            figdata_png = encode(file)
            figdata_png = adaptativeThreshold(figdata_png)
            return render_template('index_1.html' ,result1=figdata_png)    
@app.route('/video_feed', methods=['GET', 'POST'])
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if request.method == "POST":
        filtre = request.form["type_filtre"]
    return  Response(gen_frames(filtre),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/analyser', methods=['GET', 'POST'])
def analyser():
    if request.method == 'POST':
        # check if the post request has the file part
        file = request.files['file']
        if file and allowed_file(file.filename):
            figdata_png = encode(file)
            figdata_png,image_caption = analyser_image(figdata_png)
            figdata_png = base64.b64encode(figdata_png).decode('ascii')
            return render_template('index_1.html' ,result3=figdata_png,result2=image_caption)
# start flask app
app.run(host="0.0.0.0", port=5000, debug=True)
