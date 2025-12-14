import os
import numpy as np
import pandas as pd
from PIL import Image
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, render_template, request
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
result=''
model = load_model('.h5')
def model_aptos(img_path):
    img = image.load_img(img_path, target_size=(512, 512))
    img_tensor = image.img_to_array(img)                    
    img_tensor = np.expand_dims(img_tensor, axis=0)         
    img_tensor /= 255.
    pred = model.predict(img_tensor)
    preds_classes = np.argmax(pred, axis=-1)
    print(preds_classes)
    if preds_classes[0]==0:
        result = "No DR"
    elif preds_classes[0]==1:
        result = "Mild"
    elif preds_classes[0]==2:
        result = "Moderate"
    elif preds_classes[0]==3:
        result = "Severe"
    elif preds_classes[0]==4:
        result = "Proliferative DR"
    return result



