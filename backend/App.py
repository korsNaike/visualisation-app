from PIL import Image
import base64
import io
import os
import json
from datetime import datetime

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