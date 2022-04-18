# 作   者:ICloudsad
# 编写时间:2022/4/15 17:00

import torch
from torch import nn
from model.AdaLSTM import AdaLSTMCell
from model.AdaAttention import AdaAttention

class AdaDecoder(nn.Module):
    def __init__(self,num_words):
        super(AdaDecoder, self).__init__()
        self.embedding = nn.Embedding(num_words+1,512,padding_idx=0)
        self.lstmcell = AdaLSTMCell(1024,512)
        self.attention = AdaAttention()
        self.mlp = nn.Linear(512,num_words+1)
        self.softmax = nn.Softmax(dim=1)
    def forward(self,image_feature,image_total,text):
        h_t = torch.zeros((text.shape[0],512),requires_grad=True)
        m_t = torch.zeros((text.shape[0],512),requires_grad=True)
        outputs = []
        for t in range(text.shape[1]):
            text_i = self.embedding(text[:,t])
            t_v_i = torch.cat([text_i,image_total],dim=1)
            s_t,h_t,m_t = self.lstmcell(t_v_i,h_t,m_t)
            c_t_hat = self.attention(image_feature,s_t,h_t)
            output = self.softmax(self.mlp(c_t_hat+h_t))
            outputs.append(output)
        outputs = torch.stack(outputs,dim=1)
        return outputs

    def predict(self,image_feature,image_total,text,h_t,m_t):
        text_i = self.embedding(text)
        t_v_i = torch.cat([text_i, image_total], dim=1)
        s_t, h_t, m_t = self.lstmcell(t_v_i, h_t, m_t)
        c_t_hat = self.attention(image_feature, s_t, h_t)
        output = self.softmax(self.mlp(c_t_hat + h_t))
        return output,h_t,m_t





