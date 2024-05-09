import torch

from torch.nn import ReLU
from torch.autograd import Variable
from torchvision.transforms import *
from backend.visualize.utilities.utils import convert_to_grayscale
from backend.visualize.methods.BaseVisualisation import BaseVisualisation

class SaliencyMap(BaseVisualisation):

    def __init__(self, model, device):
        super().__init__(model, device)
        self.gradients = None
        self.handles = []
        self.stored_grad = False
        self.rgb2grey = Compose([ToPILImage(), Grayscale(), ToTensor()])

    def store_first_layer_grad(self):
        count = 0

        def store_grad(module, grad_in, grad_out):
            self.gradients = grad_in[0]

        for module in self.model.modules():
            if count == self.layer_number:
                self.handles.append(module.register_full_backward_hook(store_grad))
                self.stored_grad = True
            count+=1

    def guide(self, module):
        def guide_relu(module, grad_in, grad_out):
            return (torch.clamp(grad_in[0], min=0.0),)

        for module in module.modules():
            if isinstance(module, ReLU):
                self.handles.append(module.register_backward_hook(guide_relu))

    def prepare_nn(self):
        '''
        Предобработка модели
        '''
        for module in self.model.modules():
            if isinstance(module, ReLU):
                module.inplace = False

    def visualize(self, input_image, layer_number = 0, guide=False, target_class=None, regression=False):
        self.stored_grad = False
        self.layer_number = int(layer_number)
        self.model.zero_grad()
        self.prepare_nn()

        self.clean()
        if guide: self.guide(self.model)

        input_image = Variable(input_image, requires_grad=True).to(self.device)

        self.store_first_layer_grad()

        predictions = self.model(input_image)

        if target_class is None: values, target_class = torch.max(predictions, dim=1)

        if regression:
            predictions.backward(gradient=target_class, retain_graph=True)
        else:
            target = torch.zeros(predictions.size()).to(self.device)
            target[0][target_class] = 1
            predictions.backward(gradient=target, retain_graph=True)


        image = self.gradients.data.cpu().numpy()[0]
        
        image = convert_to_grayscale(image)
        image = torch.from_numpy(image).to(self.device)

        self.clean()
        self.last_target = target_class

        return image.unsqueeze(0)

