# 作   者:ICloudsad
# 编写时间:2022/4/15 19:13
from torch import nn
from model.AdaDecoder import AdaDecoder
from model.AdaEncoder import AdaEncoder

class AdaLookImageNet(nn.Module):
    def __init__(self,pretrain,num_word):
        super(AdaLookImageNet, self).__init__()
        self.encoder = AdaEncoder(pretrain)
        self.decoder = AdaDecoder(num_word)
    def forward(self,image,text):
        image_feature,image_total = self.encoder(image)
        output = self.decoder(image_feature,image_total,text)
        return output

    def predict(self,image,text,h,c):
        image_feature, image_total = self.encoder(image)
        output,h,c = self.decoder.predict(image_feature,image_total,text,h,c)
        return output,h,c