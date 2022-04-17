# 作   者:ICloudsad
# 编写时间:2022/4/11 21:19

from torch import nn
from model.Encoder import Encoder
from model.Decoder import Decoder

class LookImageNet(nn.Module):
    def __init__(self,pretrained,num_words):
        super(LookImageNet,self).__init__()
        self.encoder = Encoder(pretrained)
        self.decoder = Decoder(num_words)
    def forward(self,x):
        image,text = x
        image_feature,image_total = self.encoder(image)
        y_,lengths = self.decoder((image_feature,image_total,text))
        return y_,lengths