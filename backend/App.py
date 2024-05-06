import base64
import io
import os
import json
from datetime import datetime
import numpy as np
import torch
from torchvision.models import alexnet, vgg16, resnet18, resnet152
import torchvision.transforms.functional as TF
import torchvision.transforms as TRANSFORMS
from PIL import Image
import matplotlib.pyplot as plt
from torchvision.transforms import ToTensor, Resize, Compose

from backend.visualize.GradCam import GradCam
from .visualisation.core.utils import image_net_preprocessing, image_net_postprocessing

class App:

    def saveLoadImage(base64_image, number=0) -> str:
        '''
        Обрезать, сохранить в папку временных файлов, записать в массив json название файла,\
        и вернуть назад обрезанную версию в виде строки base64
        '''
        # Декодируем base64-строку в байтовый поток
        image_bytes = base64.b64decode(base64_image)
    
        # Открываем изображение с помощью PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Уменьшаем размер изображения
        resized_image = image.resize((224, 224))

        # Создаем временную директорию temp-images, если ее нет
        temp_dir = 'temp-images'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Генерируем уникальное имя файла
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{timestamp}.png"
        file_path = os.path.join(temp_dir, file_name)

        # Сохраняем обработанное изображение в файл
        resized_image.save(file_path, format='PNG')

        #  Кодируем обработанное изображение в base64
        with open(file_path, 'rb') as f:
            resized_image_bytes = f.read()
        resized_base64_image = base64.b64encode(resized_image_bytes).decode('utf-8')

        # Читаем существующие данные из JSON-файла
        try:
            with open('temp_files.json', 'r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            json_data = {}

        if not 'temp_files' in json_data:
            json_data["temp_files"] = []

        json_data["temp_files"][number] = file_name

        # Записываем обновленные JSON-данные в файл
        with open('temp_files.json', 'w') as f:
            json.dump(json_data, f)

        return resized_base64_image
    
    def visualize(modelName = 'VGG16', method = 'GradCam', number = 0):
        if modelName == 'VGG16':
            model = vgg16(weights='VGG16_Weights.IMAGENET1K_V1')
        
        input_image = App.getImageTensor(number)

        device = App.getDevice()
        vis = GradCam(model.to(device), device)

        img = vis.visualize(input_image.to(device), None,
          target_class=None,
          postprocessing=image_net_postprocessing,
          guide=False)
        
        return App.convertImgFromTensorToBase64(img[0])
        


    def getImageTensor(number):
        pathToImage = os.path.join(os.path.dirname(__file__), '../temp-images/' + App.getImgNameByNumber(number))
        img = Image.open(pathToImage)
        # resize the image and make it a tensor
        input_image = Compose([Resize((224,224)), ToTensor(), image_net_preprocessing])(img)
        # add 1 dim for batch
        input_image = input_image.unsqueeze(0)

        return input_image
    

    def getDevice():
        return torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
    
    def convertImgFromTensorToBase64(tensor):
        tensor = tensor.squeeze()
        if len(tensor.shape) > 2: tensor = tensor.permute(1, 2, 0)
        # Преобразование tensor в numpy array
        numpy_array = tensor.cpu().numpy()

        # Преобразование numpy array в изображение PIL
        image = Image.fromarray(np.uint8(numpy_array * 255))

        # Преобразование изображения в байтовый поток
        buffer = io.BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Кодирование байтового потока в base64
        encoded_image = base64.b64encode(buffer.read())
        encoded_image_str = encoded_image.decode('utf-8')

        return encoded_image_str
    
    def getImgNameByNumber(number):
        try:
            with open('temp_files.json', 'r') as f:
                json_data = json.load(f)
        except FileNotFoundError:
            return ''

        return json_data["temp_files"][number]
