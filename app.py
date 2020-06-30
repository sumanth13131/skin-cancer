from detect import get_img
import numpy as np
import cv2
import os

from flask import Flask,request,render_template,Response
from werkzeug.utils import secure_filename
app=Flask(__name__)

UPLOAD_FOLDER = '.\\imgssave'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template('home.html')


def img_gen():
    while True:
        frame = cv2.imread('./static/detectedimgs/detect.jpg')
        ret, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/img_feed')
def img_feed():
    return Response(img_gen(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/showimage', methods=['GET', 'POST'])
def showimage():
    if request.method == 'POST':
        try:
            for imgs in os.listdir('./imgssave/'):
                f = './imgssave/'+imgs
                os.remove(f)
        except:
            pass
        image = request.files['myfile']
        filename = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        get_img()

        return render_template('image.html')
    return render_template('home.html')

@app.route('/tech')
def tech():
    return render_template('tech.html')

@app.route('/about')
def about():
    return render_template('about.html')
    
if "__main__" == __name__:
    app.run(debug=True)