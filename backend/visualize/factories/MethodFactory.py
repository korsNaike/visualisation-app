import torch
from backend.visualize.methods import *

class MethodFactory:
        
    def __init__(self, method: str, model, device) -> None:
        self.methodObject = MethodFactory.create(method, model, device)

    def create(method: str, model, device):
        '''
        Создание объекта для визуализации
        '''
        if (method.lower() == 'gradcam'):
            return GradCam(model=model, device=device)
        
        if (method.lower() == 'deepdream'):
            return DeepDream(model=model, device=device)
        
        if (method.lower() == 'saliencymap'):
            return SaliencyMap(model=model, device=device)
        
        if (method.lower() == 'cam'):
            return Cam(model=model, device=device)
        
    def callVisualisation(self, input_image: torch.Tensor, layer_number: int, options: dict = {}):
        '''
        Вызвать визуализацию для переданной модели нейронной сети
        '''

        # Проверяем соответствие классов, в зависимости от метода загружаем опциональные параметры и вызываем метод визуализации
        if isinstance(self.methodObject, GradCam) or isinstance(self.methodObject, SaliencyMap):
            regression = bool(options.get('regression', False))
            guide = bool(options.get('guide', False))

            return self.methodObject.visualize(input_image, 
                                               layer_number, 
                                               guide=guide,
                                               regression=regression
                                               )
        
        if isinstance(self.methodObject, DeepDream):
            octaves = int(options.get('octaves', 6))
            scale_factor = float(options.get('scale_factor', 0.7))
            lr = float(options.get('lr', 0.1))
            
            return self.methodObject.visualize(input_image, 
                                               layer_number,
                                               octaves=octaves,
                                               scale_factor=scale_factor,
                                               lr=lr
                                               )
        
        if isinstance(self.methodObject, Cam):
            return self.methodObject.visualize(input_image)
        