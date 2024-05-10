import torch
import torch.nn.functional as torch_func
from torch.nn import AvgPool2d, Conv2d, Linear, ReLU

from torch.nn import ReLU
from torch.autograd import Variable
from torch.nn import Conv2d, ReLU
from backend.visualize.methods import BaseVisualisation
from backend.visualize.utilities import *

class Cam(BaseVisualisation):
    '''
    Визуализация с помощью карты активации классов.
    Проводится следующим образом:
    Сохраняется тензор выходов функции на выбранном слое, 
    извлекаются веса из последнего линейного слоя (получаем предсказание перед SoftMax), прогоняем его через SoftMax слой
    и выполняем перемножение матриц полученных выходов и весов, что и будет являться нашей картой признаков.
    '''

    def __init__(self, model, device):
        super().__init__(model, device)
        self.conv_outputs = None


    def init_hooks_for_store(self):
        '''
        Установить обработчики на слой для сохранения значений активации при прямом проходе по сети
        '''

        def store_outputs_hook(module, input, outputs):
            self.conv_outputs = outputs

        self.handles.append(self.layer.register_forward_hook(store_outputs_hook))

    def init_layers(self):
        '''
        Инициализировать последний линейный слой
        '''
        for module in self.model.modules():
            if isinstance(module, Conv2d):
                self.layer = module
            elif isinstance(module, Linear):
                self.last_linear = module

    def visualize(self, input_image):
        self.init_layers()
        self.init_hooks_for_store()

        predictions = self.model(input_image)

        target_class = self._get_target_class(predictions)
        print(self.conv_outputs.shape)
        
        _, c, h, w = self.conv_outputs.shape
        print(c, h, w)
        # Получаем веса линейного слоя
        fc_weights_class = self.last_linear.weight.data[target_class]

        # Перемножаем матрицы весов линейного слоя и выходов активаций
        print(fc_weights_class)
        cam = fc_weights_class @ self.conv_outputs.view(c, h * w)
        cam = cam.view(h, w)

        with torch.no_grad():
            image_with_heatmap = TensorHelper.combineClassActivationMap(image_net_postprocessing(input_image.squeeze().cpu()), cam)

        self.last_target = target_class
        print(self.last_target)

        return image_with_heatmap.unsqueeze(0)
    
    

    