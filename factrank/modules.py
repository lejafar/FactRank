import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class CNNText(nn.Module):

    def __init__(self, embed_num, class_num, options):
        super().__init__()
        self.opt = options

        self.embed = nn.Embedding(embed_num, self.opt.embed_dim)

        self.convs1 = nn.ModuleList([nn.Conv2d(1, self.opt.kernel_num, (kernel_size, self.opt.embed_dim)) for kernel_size in (2, 3, 4)])
        self.dropout = nn.Dropout(self.opt.dropout)
        self.fc = nn.Linear(len(self.opt.kernel_sizes) * self.opt.kernel_num, class_num)

        self.optimizer = torch.optim.Adam(self.parameters(), lr=self.options.lr, weight_decay=self.options.weight_decay)
        self.schedule = torch.optim.lr_scheduler.StepLR(self.optimizer, self.options.lr_decay_step, gamma=self.options.lr_decay)

        self.to(self.options.gpu_id)

    def set_pre_trained_word_embeddings(self, embeddings):
        self.embed = nn.Embedding.from_pretrained(embeddings, freeze=self.opt.static)

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)  # (N, Co, W)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, x):
        x = self.embed(x)  # (N, W, D)

        if self.opt.static:
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

        return self.fc(x)

