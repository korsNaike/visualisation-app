import torch
from torchvision.models import resnet152, alexnet, vgg16
from torchvision import transforms
import torchvision.transforms.functional as TF
from PIL import Image
import matplotlib.pyplot as plt
from core.SaliencyMap import SaliencyMap

# Загрузите обученную модель
# model = vgg16(weights='VGG16_Weights.IMAGENET1K_V1')
# model = resnet152(weights='ResNet152_Weights.IMAGENET1K_V1')
model = alexnet(weights='AlexNet_Weights.IMAGENET1K_V1')

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
# Создайте экземпляр класса SaliencyMap и передайте модель
saliency_map = SaliencyMap(model.to(device), device)

# Загрузите входное изображение
input_image = Image.open("X:\Studying\\visualisation-cnn\images\cat.jpg")
input_image = transforms.Resize(224)(input_image)  # Уменьшаем размер изображения до 224x224
input_image = TF.to_tensor(input_image).unsqueeze(0)

# Получите карту значимости для класса с максимальной вероятностью
saliency_map, info = saliency_map(input_image, guide=False, layer_number=1)
target_class = info['prediction'].item()

print(info)
print(saliency_map)

# Апскейлинг карты значимости до размера исходного изображения
upscaled_saliency_map = TF.resize(saliency_map, (224, 224), interpolation=Image.BICUBIC)

# Отображение результата с помощью matplotlib
def imshow(tensor):
    tensor = tensor.squeeze()
    if len(tensor.shape) > 2: tensor = tensor.permute(1, 2, 0)
    img = tensor.cpu().numpy()
    plt.imshow(img, cmap='gray')
    plt.show()

imshow(upscaled_saliency_map)
