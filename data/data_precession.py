from PIL import Image
import torch
import numpy as np
import torch.utils.data as Data

class Mydataset(Data.Dataset):
    def __init__(self,data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self,index):
        return self.data[index]

def collate_fn(data):
    filenames,text,y = zip(*data)
    X = []
    path = "data/Flicker8k_Dataset"
    for file_name in filenames:
        img = Image.open(path+"/"+ file_name).resize((224,224))
        x = np.array(img)
        #print(x.shape)
        if x.shape[-1] == 4:
            x = x[:,:,:-1]
        #print(x.shape)
        x = np.array(np.rollaxis(x,2))
        #print(x.shape)
        X.append(x)
    X = torch.tensor(X).float()
    y = [torch.tensor(_) for _ in y]
    text = [torch.tensor(_) for _ in text]
    return X,text,y

def read_data():
    with open("data/train_data",encoding="utf-8") as f:
        lines = f.readlines()
        lines = [eval(line) for line in lines]
    return lines

''''

    使用这个for batch_id,(batch_x,batch_y) in enumerate(loader)：
        batch_x: B*C*H*W    如64*3*224*224  
        batch_y: 一个列表 列表长度为batch_size 即为 64
                列表中的元素为一个序列 类型为tensor的Long类型
                类似根据下面来定义y的
                y = [torch.tensor(_) for _ in y]
'''
def get_loader(batch_size):
    data = read_data()
    dataset = Mydataset(data)
    loader = Data.DataLoader(
            dataset,
            batch_size=batch_size,
            shuffle=True,
            collate_fn=collate_fn
    )
    return loader