# 作   者:ICloudsad
# 编写时间:2022/4/15 12:24
from torch import nn
import torch

class VisualSentinel(nn.Module):
    def __init__(self,x_dim,h_dim,end_dim):
        super(VisualSentinel, self).__init__()
        self.W_x = nn.Linear(in_features=x_dim,out_features=end_dim,bias=False)
        self.W_h = nn.Linear(in_features=h_dim,out_features=end_dim,bias=False)
        self.sigmoid = nn.Sigmoid()
        self.tanh = nn.Tanh()
    def forward(self,x_t,pre_h_t,m_t):
        g_t = self.sigmoid(self.W_x(x_t)+self.W_h(pre_h_t))
        s_t = torch.mul(g_t,self.tanh(m_t))
        return s_t

