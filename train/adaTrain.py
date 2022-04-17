# 作   者:ICloudsad
# 编写时间:2022/4/15 19:20
# 作   者:ICloudsad
# 编写时间:2022/4/10 18:58
from data.data_precession import get_loader
from model.AdaLookImageNet import AdaLookImageNet
from torch import nn
import json
import torch
from torch.nn.utils import rnn
from torch.utils.tensorboard import SummaryWriter

"""
    参数区：
    epoch:学习轮数
    batch_size:批处理大小
"""
epoch = 100
batch_size = 64



use_gpu = torch.cuda.is_available()

with open("../data/word_dict",'r',encoding='utf-8') as f:
    word_dict = json.load(f)

dataloader = get_loader(batch_size)

"""
    模型构建
"""
modelnet = AdaLookImageNet(True,len(word_dict))

if use_gpu:
    modelnet = modelnet.cuda()

opt = torch.optim.Adam(modelnet.parameters(),lr=1e-4)
loss_fn = nn.CrossEntropyLoss()
"""
    训练模型
"""
writer = SummaryWriter()
iter = 0

for epoch_id in range(epoch):
    for batch_id,(picture,sentence,y,filenames) in enumerate(dataloader):
        lengths = [len(s) for s in sentence]
        text = rnn.pad_sequence(sentence, batch_first=True)
        if use_gpu:
            picture = picture.cuda()
            text = text.cuda()
        output = modelnet(picture,text)
        loss = 0
        acc = 0
        for i in range(len(sentence)):
            y_i = y[i].squeeze()
            if use_gpu:
                y_i = y_i.cuda()
            output_i = output[i,:lengths[i],:]
            loss += loss_fn(output_i,y_i)
            output_i = torch.softmax(output_i, -1)
            acc += output_i[torch.argmax(output_i,1)==y_i].shape[0]/output_i.shape[0]
        loss /= len(sentence)
        acc /= len(sentence)
        opt.zero_grad()
        loss.backward()
        opt.step()
        writer.add_scalar(f'Loss/train', loss.data, iter)
        iter += 1
        if batch_id%100==0:
            print('epoch_id:{},batch_id:{},loss:{},acc:{}'.format(epoch_id,batch_id,loss.data,acc))

    model_state = {
        'model':modelnet.state_dict(),
        'opt':opt.state_dict(),
        'epoch':epoch_id
    }
    torch.save(model_state,f"model_{epoch_id}.pt")


