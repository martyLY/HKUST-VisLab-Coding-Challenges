import torch
import torch.nn as nn
import torch.optim as optim
import torch.utils.data as data
import matplotlib.pyplot as plt
import torchvision.transforms as transforms
from PIL import Image
import pandas as pd
import numpy as np
import math
import time
import os
import gc

# Configurations
INPUT_PATH = ""
OUTPUT_PATH = ""
ORIGIN_DATA_SIZE = 12500
TARGET_DATA_SIZE = 12500
RATIO = 0.99
EPOCH = 15
BATCH_SIZE = 75
LOSS_FUNC = nn.BCELoss()
LR = 0.0001
SWITCH = 3
UPDATE = 5
TRANSFORM = transforms.Compose([transforms.Resize((256,256)),
                                transforms.RandomCrop((224,224)),
                                transforms.ToTensor(),
                                transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))
                               ])
PARAMETERS = ""

class ImageDataset(data.Dataset):
    def __init__(self, image_list, label_list):
        self.data = image_list
        self.label = label_list

    def __getitem__(self, index):
        global TRANSFORM
        img = Image.open(self.data[index])
        data = TRANSFORM(img)
        img.close()
        return data.cuda(),torch.cuda.FloatTensor([self.label[index]])

    def __len__(self):
        return len(self.data)

class VGG(nn.Module):
    def __init__(self, name="11"):
        super(VGG, self).__init__()
        self.name = "VGG"+name
        self.conv = nn.Sequential()
        i = 1; p = 1
        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=  3, out_channels= 64, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["13","16-1","16","19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels= 64, out_channels= 64, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["11-LRN"]:
            self.conv.add_module('LRN',nn.LocalResponseNorm(size=2))
        self.conv.add_module('MaxPooling-{0}'.format(p),nn.MaxPool2d(kernel_size=2, stride=2));p+=1   # 224 -> 112

        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels= 64, out_channels=128, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["13","16-1","16","19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=128, out_channels=128, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('MaxPooling-{0}'.format(p),nn.MaxPool2d(kernel_size=2, stride=2));p+=1   # 112 -> 56

        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=128, out_channels=256, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["16","19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["16-1"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=256, out_channels=256, kernel_size=1, stride=1, padding=0))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('MaxPooling-{0}'.format(p),nn.MaxPool2d(kernel_size=2, stride=2));p+=1   # 56 -> 28

        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=256, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["16","19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["16-1"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=1, stride=1, padding=0))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('MaxPooling-{0}'.format(p),nn.MaxPool2d(kernel_size=2, stride=2));p+=1   # 28 -> 14

        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
        self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["16","19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["16-1"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=1, stride=1, padding=0))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        if name in ["19"]:
            self.conv.add_module('conv-{0}'.format(i),nn.Conv2d(in_channels=512, out_channels=512, kernel_size=3, stride=1, padding=1))
            self.conv.add_module('ReLU-{0}'.format(i),nn.ReLU());i+=1
        self.conv.add_module('MaxPooling-{0}'.format(p),nn.MaxPool2d(kernel_size=2, stride=2));p+=1   # 14 -> 7

        self.fc = nn.Sequential(
            nn.Linear(512*7*7,4096),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(4096,4096),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(4096,1000),
            nn.ReLU(),
            nn.Linear(1000,1),
            nn.Sigmoid()
        )

    def forward(self, x):
        x = self.conv(x)
        x = x.view(x.shape[0], -1)
        x = self.fc(x)
        return x

def train(optimizer):
    global net
    global EPOCH
    global BATCH_SIZE
    global train_data
    global validate_data
    global PROGRAM_START
    print('['+net.name+'] with optimizer ['+str(type(optimizer))+']:')
    train_loader = data.DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    validate_loader = data.DataLoader(validate_data, batch_size=1, shuffle=False, num_workers=0)
    BATCH = len(train_loader)
    m = len(validate_loader)
    for epoch in range(EPOCH):
        EPOCH_START = time.time()
        print("\tEpoch #{0}/{1}:".format(epoch+1,EPOCH))
        for batch,(x,y) in enumerate(train_loader):
            optimizer.zero_grad()
            t = net(x)
            loss = LOSS_FUNC(t,y)
            print("\t\tBatch #{0}/{1}: ".format(batch+1,BATCH) + "Loss = %.6f"%float(loss))
            loss.backward()
            optimizer.step()
        with torch.no_grad():
            L = 0.
            E = 0.
            for batch,(x,y) in enumerate(validate_loader):
                t = net(x)
                L += float(LOSS_FUNC(t,y))
                E += float((float(t[0][0])>0.5)!=y)
            print("\t  Validation Loss = %.6f. Error Rate = %.3f%%"%(L/m,E*100/m))
            if((epoch+1)%UPDATE==0):
                torch.save(net.state_dict(),OUTPUT_PATH+"/{0}[{1}]".format(net.name,epoch+1)+"-L(%.6f)E(%.3f).pt"%(L/m,E*100/m))
                torch.save(optimizer.state_dict(),OUTPUT_PATH+"/{0}[{1}]".format(net.name,epoch+1)+"-L(%.6f)E(%.3f)-optimizer.pt"%(L/m,E*100/m))
        print("\t  Finish epoch #{0}".format(epoch+1)+" in %.4f s."%(time.time()-EPOCH_START)+" Total Time Cost = %.4f s."%(time.time()-PROGRAM_START))

def run(filename):
    global net
    global test_data
    prediction = []
    test_loader = data.DataLoader(test_data, batch_size=1, shuffle=False, num_workers=0)
    with torch.no_grad():
        for i,(x,y) in enumerate(test_loader):
            t = net(x)
            prediction.append([i+1,float(t[0][0])])
    submission = pd.DataFrame(prediction)
    submission.columns = ['id','label']
    submission.to_csv(filename+".csv",index=0)

def load():
    np.random.seed(998244353)
    torch.manual_seed(998244353)
    image_list = []
    label_list = []
    for i in range(ORIGIN_DATA_SIZE):
        image_list.append(INPUT_PATH+"/train/cat.{0}.jpg".format(i))
        label_list.append(0)
        image_list.append(INPUT_PATH+"/train/dog.{0}.jpg".format(i))
        label_list.append(1)
    n = int(ORIGIN_DATA_SIZE*2*RATIO)
    train_data = ImageDataset(image_list[:n],label_list[:n])
    validate_data = ImageDataset(image_list[n:],label_list[n:])
    image_list = []
    for i in range(TARGET_DATA_SIZE):
        image_list.append(INPUT_PATH+"/test/{0}.jpg".format(i+1))
    test_data = ImageDataset(image_list,[0]*TARGET_DATA_SIZE)
    # np.random.seed()
    # torch.seed()
    return train_data,validate_data,test_data

print("*****Start")
PROGRAM_START = time.time()
train_data,validate_data,test_data = load()
print("Finish reading data in %.4f s."%(time.time()-PROGRAM_START))
net = VGG("19")
if SWITCH//2==1 and PARAMETERS!="":
    net.load_state_dict(torch.load(PARAMETERS+".pt"))
    print("Load Model ["+PARAMETERS+".pt] Success!")
net.cuda()
optimizer = optim.RMSprop(net.parameters(), lr=LR, alpha=0.9)
if SWITCH//2==1 and PARAMETERS!="":
    optimizer.load_state_dict(torch.load(PARAMETERS+"-optimizer.pt"))
    print("Load Optimizer ["+PARAMETERS+"-optimizer.pt] Success!")
LOSS_FUNC.cuda()
if SWITCH% 2==1:
    train(optimizer)
TRANSFORM = transforms.Compose([transforms.Resize((224,224)),
                                transforms.ToTensor(),
                                transforms.Normalize((0.485,0.456,0.406),(0.229,0.224,0.225))
                               ])
run(OUTPUT_PATH+"/{0}".format(net.name))
print("*****Finish")