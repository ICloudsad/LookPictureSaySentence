# 作   者:ICloudsad
# 编写时间:2022/4/15 12:17
from torch import nn
from model.VisualSentinel import VisualSentinel

class AdaLSTMCell(nn.Module):
    def __init__(self,input_size,hidden_size):
        super(AdaLSTMCell, self).__init__()
        self.lstmcell = nn.LSTMCell(input_size,hidden_size)
        self.sentinel = VisualSentinel(input_size,hidden_size,hidden_size)
    def forward(self,x_t,pre_h_t,pre_c_t):
        h_t,c_t = self.lstmcell(x_t,(pre_h_t,pre_c_t))
        s_t = self.sentinel(x_t,pre_h_t,c_t)
        return s_t,h_t,c_t

