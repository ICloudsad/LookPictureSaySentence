from PIL import Image
import torch
import numpy as np
import torch.utils.data as Data
from torchvision.transforms import transforms


class Mydataset(Data.Dataset):
    def __init__(self, data):
        self.data = data
        self.transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.485, 0.456, 0.406),
                                 (0.229, 0.224, 0.225))]
        )
        self.path_flickr = "../input/flickr-image-dataset/flickr30k_images/flickr30k_images"
        self.path_coco = "../input/coco2014/train2014/train2014"

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        filename, text, y = self.data[index]
        if filename.startswith("COCO"):
            img = Image.open(self.path_coco + "/" + filename).convert("RGB").resize((224, 224))
        else:
            img = Image.open(self.path_flickr + "/" + filename).convert("RGB").resize((224, 224))
        img = self.transform(img)
        y = torch.tensor(y)
        text = torch.tensor(text)
        return img, text, y, filename


def collate_fn(data):
    img, text, y, filename = zip(*data)
    img = torch.stack(img, dim=0)
    return img, text, y, filename


def read_data():
    with open("../input/lookimage2/train_data_2", encoding="utf-8") as f:
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
        collate_fn=collate_fn,
        pin_memory=True
    )
    return loader