import torch
from backend.visualize.GradCam import GradCam

class MethodFactory:
        
    def __init__(self, method: str, model, device) -> None:
        self.methodObject = MethodFactory.create(method, model, device)

    def create(method: str, model, device):
        '''
        Создание объекта для визуализации
        '''
        if (method.lower() == 'gradcam'):
            return GradCam(model=model, device=device)
        
    def callVisualisation(self, input_image: torch.Tensor, layer_number: int, options: dict = {}):
        '''
        Вызвать визуализацию для переданной модели нейронной сети
        '''
        if isinstance(self.methodObject, GradCam):
            regression = bool(options.get('regression', False))
            guide = bool(options.get('guide', False))
            return self.methodObject.visualize(input_image, 
                                               layer_number, 
                                               guide=guide,
                                               regression=regression
                                               )