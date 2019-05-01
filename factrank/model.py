import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class CNNText(nn.Module):

    def __init__(self, embed_num, class_num, embed_dim=320, kernel_num=100, kernel_sizes=(3, 4, 5), dropout=1, static=True, pre_trained_word_embeddings=None):
        super().__init__()

        if pre_trained_word_embeddings:
            self.embed = nn.Embedding.from_pretrained(pre_trained_word_embeddings, freeze=static)
        else:
            self.embed = nn.Embedding(embed_num, embed_dim)

        self.convs1 = nn.ModuleList([nn.Conv2d(1, kernel_num, (kernel_size, embed_dim)) for kernel_size in kernel_sizes])
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(len(kernel_sizes) * kernel_num, class_num)

        self.fc_factual = nn.Linear(len(kernel_sizes) * kernel_num, 1) # binary
        self.fc_relevant = nn.Linear(len(kernel_sizes) * kernel_num, 1) # binary
        self.fc_checkworthy = nn.Linear(2, class_num)

        self.static = static

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)  # (N, Co, W)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, x):
        x = self.embed(x)  # (N, W, D)

        if self.static:
            x = Variable(x)

        x = x.unsqueeze(1)  # (N, Ci, W, D)

        x = [F.relu(conv(x)).squeeze(3) for conv in self.convs1]  # [(N, Co, W), ...]*len(Ks)
        x = [F.max_pool1d(i, i.size(2)).squeeze(2) for i in x]  # [(N, Co), ...]*len(Ks)
        x = torch.cat(x, 1)
        '''
        x1 = self.conv_and_pool(x,self.conv13) #(N,Co)
        x2 = self.conv_and_pool(x,self.conv14) #(N,Co)
        x3 = self.conv_and_pool(x,self.conv15) #(N,Co)
        x = torch.cat((x1, x2, x3), 1) # (N,len(Ks)*Co)
        '''
        x = self.dropout(x)  # (N, len(Ks)*Co)

        self.factual = self.fc_factual(x)
        self.relevance = self.fc_relevant(x)
        self.checkworthy = self.fc_checkworthy(torch.cat((self.factual, self.relevance), 1))  # (N, C)

        return self.fc(x)
