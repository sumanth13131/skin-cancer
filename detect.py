import numpy as np
import cv2
import os
from PIL import Image
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
model=load_model('model.h5')


def get_img():
    f = []
    for file in os.listdir('./imgssave/'):
        f.append(file)
    path = "./imgssave/"+f[0]
    print(path)
    img=cv2.imread(path)
    img_size=cv2.resize(img,(224,224))
    image = img_to_array(img_size)
    frame = preprocess_input(image)
    frame = np.expand_dims(frame, axis=0)
    pred=model.predict(frame)
    print(pred)
    cla = np.argmax(pred[0])
    label = "benign" if cla == 0 else "malignant"
    color = (0, 255, 0) if cla == 0 else (0, 0, 255)

	# include the probability in the label
    label = "{}: {:.3f}%".format(label, max(pred[0]) * 100)
    # cv2.putText(img, label, (10,10),
    #                 cv2.FONT_HERSHEY_SIMPLEX,0.5 , color, 2)
    
    try:
        for i in os.listdir('./static/detectedimgs/'):
            file = './imgssave/detectedimgs/'+i
            os.remove(file)
    except:
        pass

    img=cv2.resize(img,(900,600))
    cv2.putText(img, label, (20,20),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8 , color, 2)
    cv2.imwrite('./static/detectedimgs/detect.jpg', img)
    
