# Описание

Приложение с веб-интерфейсом для визуализации работы нейронных сетей, решающих задачу классификации.

# Установка

## Через pip
```
pip install -r requirements.txt
pip3 install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
```

## Через Poetry
```
poetry install
```
### Поддержка CUDA
```
poetry add torch==2.3.0+cu121 --source torch
```