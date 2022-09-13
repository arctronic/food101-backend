from __future__ import print_function, division
import io
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
import torch.backends.cudnn as cudnn
import numpy as np
import torchvision
from torchvision import datasets, transforms
import torchvision.models as models
import time
import os
import copy
from PIL import Image
import timm
from food_list import label_mapping

criterion = nn.CrossEntropyLoss()

PATH1 = './model/food101-efficientNetV2.pt'
efficientNetV2_model = timm.create_model(
    'tf_efficientnetv2_m_in21k', pretrained=True)
num_ftrs = efficientNetV2_model.classifier.in_features
efficientNetV2_model.classifier = nn.Linear(num_ftrs, 101)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
efficientNetV2_model.load_state_dict(torch.load(PATH1, map_location=device))
efficientNetV2_model.to(device)
efficientNetV2_model.eval()


def transform_image(image_bytes):
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

    image = Image.open(io.BytesIO(image_bytes))
    return transform(image).unsqueeze(0)


def prediction_random_images(images):
    for img in images:
        img  = transform_image(img)
        outputs = efficientNetV2_model(img)
        _, predicted = torch.max(outputs.data, 1)
        return label_mapping[predicted.item()]
