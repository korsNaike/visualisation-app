import torch
from torchvision.models import resnet152, alexnet, vgg16, resnet18

class ModelFactory:

    def create(model: str) -> torch.nn.Module:
        if model.lower() == 'vgg16':
            return vgg16(weights='VGG16_Weights.IMAGENET1K_V1')
        
        if model.lower() == 'resnet152':
            return resnet152(weights='ResNet152_Weights.IMAGENET1K_V1')
        
        if model.lower() == 'alexnet':
            return alexnet(weights='AlexNet_Weights.IMAGENET1K_V1')
        
        if model.lower() == 'resnet18':
            return resnet18(weights='ResNet18_Weights.IMAGENET1K_V1')
        
        return False