# Description

An application with a web interface for visualizing the work of neural networks solving the classification problem.
In the application, you can select one of the pre-trained ImageNet 1k models, select 1 of the visualization methods among CAM, GradCam, Saliency map, DeepDreap, configure visualization parameters, upload an image and see the visualization result.

# Installation

## pip
```
pip install -r requirements.txt
pip3 install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
```

## Poetry
```
poetry install
```
### CUDA support
```
poetry add torch==2.3.0+cu121 --source torch
```
