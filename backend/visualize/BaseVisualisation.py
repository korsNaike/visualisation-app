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
        for module in self.model.modules():
                if i == layer_number:
                    self.layer = module
                    return
                i += 1