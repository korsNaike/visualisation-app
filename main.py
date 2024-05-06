import eel
from PIL import Image
import base64
import io
import os
import json
from datetime import datetime
from backend.App import App

@eel.expose
def loadImage(base64_image, number = 0):
    return App.saveLoadImage(base64_image=base64_image, number=number)

@eel.expose
def visualize(model = 'VGG16', method = 'GradCam', number = 0):
    return App.visualize(modelName=model, method=method, number=number)


eel.init('web')

eel.start('main.html', size=(1200, 800))