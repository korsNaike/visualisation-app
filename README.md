# Description

An application with a web interface for visualizing the work of neural networks solving the classification problem.

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
