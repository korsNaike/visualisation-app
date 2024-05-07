from abc import abstractmethod
from typing import Any

from torch import Tensor


class BaseVisualisation:
    def __init__(self, model, device):
        self.model, self.device = model, device
        self.handles = []

    def clean(self):
        [h.remove() for h in self.handles]

    @abstractmethod
    def visualize(self, input_image, layer_number, *args: Any, **kwds: Any) -> Tensor:
        pass

    def init_layer_by_number(self, layer_number: int):
        '''
        Инициализация поля self.layer по номеру слоя в модели
        '''
        i = 0
        layer_number = int(layer_number)
        print('нужно: ' + str(layer_number))
        for module in self.model.modules():
            print(str(i) + ' сравним ? ' + str(layer_number) + '\n')
            if i == layer_number:
                print("попали, модуль номер = " + str(i) + ' ' +  str(module.__class__.__name__))
                self.layer = module
                return
            i += 1