# 作   者:ICloudsad
# 编写时间:2022/4/15 17:01
import torch
from torch import nn
from torchvision.models import resnet152
from torch.nn import Sequential

class AdaEncoder(nn.Module):
    def __init__(self,pretrained):
        super(AdaEncoder, self).__init__()
        resnet = resnet152(pretrained)
        self.resnet_conv = Sequential(*list(resnet.children())[:-2])
        self.avgpool = nn.AdaptiveAvgPool2d(output_size=(1,1))
        self.feature_fc = nn.Linear(2048,512)
        self.total_fc = nn.Linear(2048,512)
        self.dropout = nn.AlphaDropout(0.5)
        self.relu = nn.ReLU()
    def forward(self,images):
        images_conv = self.resnet_conv(images)
        images_total = self.avgpool(images_conv).view(images.shape[0],2048)
        images_total = self.relu(self.total_fc(self.dropout(images_total)))
        images_feature = images_conv.view(images_conv.shape[0],images_conv.shape[1],-1).permute(0,2,1).reshape(-1,2048)
        images_feature = self.relu(self.feature_fc(self.dropout(images_feature))).view(images.shape[0],49,512)
        return images_feature,images_total


