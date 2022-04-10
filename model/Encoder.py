# 作   者:ICloudsad
# 编写时间:2022/4/10 16:02
import torch
from torchvision.models import resnet152
from torch.nn import Sequential
from torch import nn
import numpy as np

# # 获取图片部分向量与全部向量
# def get_resnet(pretrained=False):
#     resnet = resnet152(pretrained=pretrained)
#     # 特征向量
#     image_features_model = Sequential(
#         resnet.conv1,
#         resnet.maxpool,
#         resnet.layer1,
#         resnet.layer2,
#         resnet.layer3,
#         resnet.layer4
#     )
#     image_total_model = Sequential(
#         image_features_model,
#         nn.Conv2d(2048,1024,1),
#         nn.Conv2d(1024,512,1),
#         nn.Conv2d(512,512,3,2),
#         nn.Conv2d(512,256,1),
#         nn.Conv2d(256,256,3,2),
#     )
#     return image_features_model,image_total_model


class Encoder(nn.Module):
    def __init__(self,pretrained):
        super(Encoder,self).__init__()
        resnet = resnet152(pretrained=pretrained)
        # 特征向量
        self.image_features_model = Sequential(
            resnet.conv1,
            resnet.maxpool,
            resnet.layer1,
            resnet.layer2,
            resnet.layer3,
            resnet.layer4
        )
        self.image_total_model = Sequential(
            nn.Conv2d(2048, 1024, 1),
            nn.Conv2d(1024, 512, 1),
            nn.Conv2d(512, 512, 3, 2),
            nn.Conv2d(512, 256, 1),
            nn.Conv2d(256, 256, 3, 2),
        )
        self.fc1 = nn.Linear(2048,1024)
        self.relu = nn.ReLU()
        self.drop1 = nn.AlphaDropout()
        self.fc2 = nn.Linear(1024,512)
        self.drop2 = nn.AlphaDropout()
        self.fc3 = nn.Linear(512,256)

    def forward(self,x):
        image_features = self.image_features_model(x)
        image_total = self.image_total_model(image_features).reshape([image_features.shape[0],1,-1])
        image_features = image_features.view(image_features.shape[0],image_features.shape[1],-1).permute(0,2,1)
        image_features = self.fc1(image_features)
        image_features = self.relu(image_features)
        image_features = self.drop1(image_features)
        image_features = self.fc2(image_features)
        image_features = self.relu(image_features)
        image_features = self.drop2(image_features)
        image_features = self.fc3(image_features)
        image_features = self.relu(image_features)
        return image_features,image_total

