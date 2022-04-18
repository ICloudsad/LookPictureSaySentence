# 作   者:ICloudsad
# 编写时间:2022/4/15 11:59
import torch
from torch import nn

class AdaAttention(nn.Module):
    def __init__(self):
        super(AdaAttention, self).__init__()
        self.W_s = nn.Linear(512,49,bias=False)
        self.W_g = nn.Linear(512,49,bias=False)
        self.W_h = nn.Linear(49,1,bias=False)
        self.W_v = nn.Linear(512,49,bias=False)
        self.tanh = nn.Tanh()
        self.softmax = nn.Softmax(dim=1)
    def forward(self,V,s_t,h_t):
        # V:64*49*512  s_t:64*512 h_t:64*512
        V = V.contiguous().view(-1,V.shape[2])
        z_t = self.W_h(self.tanh((self.W_v(V).view((s_t.shape[0],49,49))+self.W_g(h_t).unsqueeze(1).expand((s_t.shape[0],49,49))).contiguous().view(-1,49))).view((s_t.shape[0],49)) # 64*49
        beta_t = self.W_h(self.tanh(self.W_s(s_t)+self.W_g(h_t))) # 64*1
        z_t_hat = torch.cat([z_t,beta_t],dim=1)
        alpha_hat = self.softmax(z_t_hat).unsqueeze(2).expand(s_t.shape[0],50,512)
        V_s = torch.cat([V.view(s_t.shape[0],49,512),s_t.unsqueeze(1)],dim=1) # 64*50*512
        c_t_hat = torch.sum(torch.mul(alpha_hat,V_s),dim=1) # 64*512
        return c_t_hat
