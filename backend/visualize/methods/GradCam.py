import torch
import torch.nn.functional as torch_func

from torch.nn import ReLU
from torch.autograd import Variable
from torch.nn import Conv2d, ReLU
from backend.visualize.methods import BaseVisualisation
from backend.visualize.utilities import *

class GradCam(BaseVisualisation):

    def __init__(self, model, device):
        super().__init__(model, device)
        self.gradients = None
        self.conv_outputs = None

    def init_hooks_for_store(self):
        '''
        Установить обработчики на слой для сохранения значений активации при прямом и обратном проходе по сети
        '''
        def store_grads(module, grad_in, grad_out):
            self.gradients = grad_out[0]

        def store_outputs(module, input, outputs):
            if module == self.layer:
                self.conv_outputs = outputs

        self.handles.append(self.layer.register_forward_hook(store_outputs))
        self.handles.append(self.layer.register_backward_hook(store_grads))

    def set_guide(self):
        '''
        Устанавливаем обработчик на слои ReLu при обратном проходе на градиенты ReLu функцию max(0, X).
        Для метода Guided GradCam
        '''
        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_out[0], min=0.0),)

        for module in self.model.modules():
            if isinstance(module, ReLU):
                self.handles.append(module.register_backward_hook(guide_relu))

    def init_default_layer(self):
        '''
        Инициализация слоя для визуализации
        '''
        for module in self.model.modules():
            if isinstance(module, Conv2d):
                self.layer = module
    

    def visualize(self, input_image, layer_number=None, guide=False, regression=False) -> torch.Tensor:
        '''
        Основной вызов для визуализации работы сети
        '''
        self.clean()
        self.model.zero_grad()

        if layer_number is None:
            self.init_default_layer()
        else:
            self.init_layer_by_number(layer_number)

        self.init_hooks_for_store()

        if guide:
            self.set_guide()

        predictions = self.__get_predictions(input_image=input_image)
        target_class = self._get_target_class(predictions)

        if regression: 
            predictions.backward(gradient=target_class, retain_graph=True)
        else:
            target = torch.zeros(predictions.size()).to(self.device)
            target[0][target_class] = 1
            predictions.backward(gradient=target, retain_graph=True)

        with torch.no_grad():
            # уменьшаем размерность тензора до 1x1 путём адаптивного усреднения
            avg_channel_grad = torch_func.adaptive_avg_pool2d(self.gradients.data, 1)
            # пропускаем через relu полученные значения слоя и средние значения градиента для того, чтобы вычислить карту активаций
            self.cam = torch_func.relu(torch.sum(self.conv_outputs[0] * avg_channel_grad[0], dim=0))

            image_with_heatmap = TensorHelper.combineClassActivationMap(image_net_postprocessing(input_image.squeeze().cpu()), self.cam)

        self.clean()
        self.last_target = target_class

        return image_with_heatmap.unsqueeze(0)

    def __get_predictions(self, input_image):
        data_for_input = Variable(input_image, requires_grad=True).to(self.device)
        return self.model(data_for_input)
    


