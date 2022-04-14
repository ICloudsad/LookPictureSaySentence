# 作   者:ICloudsad
# 编写时间:2022/4/10 20:21
import torch
from torch import nn
from torch.nn.utils import rnn

class Decoder(nn.Module):
    def __init__(self,num_words):
        super(Decoder,self).__init__()
        self.embedding = nn.Embedding(num_words+1,256,padding_idx=0)
        self.lstm_text = nn.LSTM(256,256,num_layers=2,batch_first=True)
        self.lstm_image = nn.LSTM(256,256,num_layers=2,batch_first=True)
        self.attention = nn.MultiheadAttention(256,1,batch_first=True)
        self.fc = nn.Linear(256,num_words+1)
    def forward(self,x):
        """
        image_feature:图片的部分特征向量
        image_total:图片的总体特征向量
        text:文本的index列表
        """
        use_gpu = torch.cuda.is_available()

        image_feature,image_total,text = x
        # 对image_feature进行lstm提取h,c

        # 对text进行padding
        lengths = [len(s) for s in text]
        lengths = torch.Tensor(lengths)
        _, idx_sort = torch.sort(lengths, dim=0, descending=True)
        _, idx_unsort = torch.sort(idx_sort, dim=0)
        text = rnn.pad_sequence(text, batch_first=True)
        if use_gpu:
            text = text.cuda()
            lengths = lengths.cuda()
            idx_sort = idx_sort.cuda()
            idx_unsort = idx_unsort.cuda()
        text = text.index_select(0, idx_sort)
        lengths = lengths[idx_sort]
        image_feature = image_feature.index_select(0,idx_sort)
        image_total = image_total.index_select(0,idx_sort)
        _,(h,c) = self.lstm_image(image_total)
        # 对text进行embedding
        text = self.embedding(text.long())
        text = rnn.pack_padded_sequence(text,lengths.cpu(),batch_first=True)

        # 将text向量进行lstm，初始h,c使用图片lstm的h,c
        text,(h_,c_) = self.lstm_text(text,(h,c))
        text,_ = rnn.pad_packed_sequence(text,batch_first=True)

        # 使用attention对图像进行注意力，key:图像向量  query:文本向量  value:图像向量
        attn_out,att_wight = self.attention(text,image_feature,image_feature)

        y_ = self.fc(attn_out)
        y_ = y_.index_select(0,idx_unsort)
        lengths = lengths.index_select(0,idx_unsort)
        return y_,lengths

