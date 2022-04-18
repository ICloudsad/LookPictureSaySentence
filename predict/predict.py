# 作   者:ICloudsad
# 编写时间:2022/4/11 13:20
from data.data_precession import get_loader
from model.AdaLookImageNet import AdaLookImageNet
import torch
import json
import copy
from torchvision.transforms import transforms
from PIL import Image

batch_size = 1
max_length = 50

use_gpu = torch.cuda.is_available()

with open("../data/word_dict",'r',encoding='utf-8') as f:
    word_dict = json.load(f)

idx2word = [w for w in word_dict.keys()]

net = AdaLookImageNet(True,len(word_dict))
net.load_state_dict(torch.load("../logs/model_45.pt",map_location=torch.device('cpu'))['model'])

data_loader = get_loader(batch_size)
net = net.eval()

if use_gpu:
    net = net.cuda()


def predict(image,word,h,c):
    y_,h,c = net.predict(image, word,h,c)
    y_ = y_.reshape(-1)
    scores = torch.log(torch.softmax(y_,dim=0))
    scores, idx = torch.sort(scores, descending=True)
    scores = scores[:3].tolist()
    max_idx = idx[:3]
    return max_idx,scores,h,c

def lookimage(path):
    image = Image.open(path).convert("RGB").resize((224, 224))
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.485, 0.456, 0.406),
                             (0.229, 0.224, 0.225))]
    )
    image = transform(image)
    image = image.unsqueeze(0)
    h = torch.zeros((1,512),requires_grad=True)
    c = torch.zeros((1,512),requires_grad=True)
    if use_gpu:
        image = image.cuda()
    word = [[word_dict['__start__']] for _ in range(3)]
    words = torch.Tensor(word[0]).long()
    max_three_idx, total_score,h,c = predict(image, words,h,c)
    end_score_list = []
    end_seq_list = []
    best_score_list = []
    best_seq_list = []
    best_seq_list.extend(max_three_idx.tolist())
    best_seq_list = [[s] for s in best_seq_list]
    best_score_list.extend(total_score)
    flag = 3
    while True:
        max_idx_list_temp = []
        score_list_temp = []
        p = 0 # 防止pop时溢出
        not_end_idx_list = []
        for i,idx in enumerate(max_three_idx):
            if idx == word_dict['__end__']:
                # 当预测的是end时，将对应的序列和分数加入到end列表中
                # 同时在best列表中删除
                end_seq_list.append(best_seq_list[i-p])
                end_score_list.append(best_score_list[i-p])
                best_seq_list.pop(i-p)
                best_score_list.pop(i-p)
                p += 1
            if idx != word_dict['__end__']:
                not_end_idx_list.append(idx)
        if len(not_end_idx_list) != 0:
            best_score_list_copy_temp = copy.deepcopy(best_score_list)
            best_seq_list_copy_temp = copy.deepcopy(best_seq_list)
            for _ in range(2):
                best_score_list_copy = copy.deepcopy(best_score_list_copy_temp)
                best_seq_list_copy = copy.deepcopy(best_seq_list_copy_temp)
                best_seq_list.extend(best_seq_list_copy)
                best_score_list.extend(best_score_list_copy)
            for k, idx in enumerate(not_end_idx_list):
                words = torch.tensor([idx.item()]).long()
                max_three_idx, score,h,c = predict(image, words,h,c)
                for i,next_idx in enumerate(max_three_idx):
                    best_seq_list[i*len(not_end_idx_list)+k].append(next_idx.item())
                    best_score_list[i*len(not_end_idx_list)+k] += score[i]
        else:
            break
        best_seq_list = torch.Tensor(best_seq_list)
        best_score_list = torch.Tensor(best_score_list)
        sort_score,sort_idx = torch.sort(best_score_list,descending=True)
        sort_seq =best_seq_list.index_select(0,sort_idx)[:3].tolist()
        sort_score = sort_score[:3].tolist()
        best_score_list = sort_score
        best_seq_list = sort_seq
        max_three_idx = torch.Tensor([l[-1] for l in best_seq_list])
        if len(best_seq_list[0]) > max_length:
            break
    for i in range(len(end_seq_list)):
        end_score_list[i] = end_score_list[i]/len(end_seq_list[i])
    end_score_list = torch.Tensor(end_score_list)
    _,sort_idx = torch.sort(end_score_list,descending=True)
    if len(end_seq_list[sort_idx[0].item()]) != 0:
        best_seq = ' '.join([idx2word[int(s)-1] for s in end_seq_list[sort_idx[0].item()][:-1]])
    else:
        best_seq = ' '.join([idx2word[int(s) - 1] for s in end_seq_list[sort_idx[1].item()][:-1]])
    return best_seq