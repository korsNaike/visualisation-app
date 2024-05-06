import cv2
import numpy as np
import torch


class TensorHelper:

    def combineClassActivationMap(image: torch.Tensor, cam: torch.Tensor):
        '''
        Совместить тензор изображения и карты активаций, предварительно нормализовав изображение и карту
        '''
        image_with_heatmap = TensorHelper.combineImageAndMap(image.squeeze().permute(1,2,0).cpu().numpy(),
              cam.detach().cpu().numpy())

        return torch.from_numpy(image_with_heatmap).permute(2,0,1)

    
    def combineImageAndMap(image, cam):
        '''
        Совместить тензор изображения и карты активаций
        '''
        h, w, _ = image.shape
        cam -= np.min(cam)
        cam /= np.max(cam)  # Normalize between 0-1
        cam = cv2.resize(cam, (w,h))
    
        cam = np.uint8(cam * 255.0)
        img_with_cam = cv2.applyColorMap(cam, cv2.COLORMAP_JET)
        img_with_cam = cv2.cvtColor(img_with_cam, cv2.COLOR_BGR2RGB)
        img_with_cam = img_with_cam + (image * 255)
        img_with_cam /= np.max(img_with_cam)
    
        return img_with_cam
        