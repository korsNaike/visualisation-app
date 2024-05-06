import torch
from torchvision.models import alexnet, vgg16, resnet18, resnet152
import torchvision.transforms.functional as TF
import torchvision.transforms as TRANSFORMS
from PIL import Image
import matplotlib.pyplot as plt

from core.DeepDream import DeepDream

# Загрузите обученную модель
# model = vgg16(weights='VGG16_Weights.IMAGENET1K_V1')
# model = resnet152(weights='ResNet152_Weights.IMAGENET1K_V1')
model = alexnet(weights='AlexNet_Weights.IMAGENET1K_V1')

# Замораживаем градиенты для всех слоев, кроме выбранного
for param in model.parameters():
    param.requires_grad = False

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Инициализация класса DeepDream
deep_dream = DeepDream(model.to(device), device)

# Выбор слоя для визуализации (в ResNet доступны layer1, layer2, layer3, layer4)
countLayer = 0
layerNumber = 10
for i in model.modules():
    if (countLayer == layerNumber):
        layer = i
    countLayer+=1

print(layer)

# Загрузка и предобработка входного изображения
img = Image.open("X:\Studying\\visualisation-cnn\images\dog_and_cat.jpg")
img = TRANSFORMS.Resize(224)(img)  # Уменьшаем размер изображения до 224x224
img = TF.to_tensor(img).unsqueeze(0)

# Вызов DeepDream
output, _ = deep_dream(img, layer, octaves=6, scale_factor=0.7, lr=0.1)

print(output)
# Отображение результата с помощью matplotlib
def imshow(tensor):
    tensor = tensor.squeeze()
    if len(tensor.shape) > 2: tensor = tensor.permute(1, 2, 0)
    img = tensor.cpu().numpy()
    plt.imshow(img)
    plt.show()

imshow(output)
