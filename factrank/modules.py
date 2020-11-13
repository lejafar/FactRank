import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class CNNText(nn.Module):

    def __init__(self, embed_num, class_num, options, pretrained_vec=None):
        super().__init__()
        self.options = options

        self.embed = nn.Embedding(embed_num, self.options.embed_dim)

        self.conv12 = nn.Conv2d(1, self.options.kernel_num, (2, self.options.embed_dim))
        self.conv13 = nn.Conv2d(1, self.options.kernel_num, (3, self.options.embed_dim))
        self.conv14 = nn.Conv2d(1, self.options.kernel_num, (4, self.options.embed_dim))
        self.conv15 = nn.Conv2d(1, self.options.kernel_num, (5, self.options.embed_dim))
        self.conv16 = nn.Conv2d(1, self.options.kernel_num, (6, self.options.embed_dim))

        if self.options.n_layers > 1:
            # second layer
            self.conv22 = nn.Conv2d(1, 2 * self.options.kernel_num, (3, self.options.kernel_num))
            self.conv23 = nn.Conv2d(1, 2 * self.options.kernel_num, (3, self.options.kernel_num))
            self.conv24 = nn.Conv2d(1, 2 * self.options.kernel_num, (3, self.options.kernel_num))
            self.conv25 = nn.Conv2d(1, 2 * self.options.kernel_num, (3, self.options.kernel_num))
            self.conv26 = nn.Conv2d(1, 2 * self.options.kernel_num, (3, self.options.kernel_num))

        if self.options.n_layers > 2:
            # third layer
            self.conv33 = nn.Conv2d(1, 2 * self.options.kernel_num, (3, 3 * self.options.kernel_num))

        self.dropout = nn.Dropout(self.options.dropout)
        self.fc = nn.Linear((self.options.n_layers * 5) * self.options.kernel_num, class_num)

        self.optimizer = torch.optim.Adam(self.parameters(), lr=self.options.lr, weight_decay=self.options.weight_decay)
        self.schedule = torch.optim.lr_scheduler.StepLR(self.optimizer,
                                                        self.options.lr_decay_step,
                                                        gamma=self.options.lr_decay)

        self.to(self.options.gpu_id)

    def set_pre_trained_word_embeddings(self, embeddings):
        self.embed = nn.Embedding.from_pretrained(embeddings, freeze=self.options.static)

    def conv_and_pool(self, x, conv):
        x = F.relu(conv(x)).squeeze(3)  # (N, Co, W)
        x = F.max_pool1d(x, x.size(2)).squeeze(2)
        return x

    def forward(self, x):
        x = self.embed(x)  # (N, W, D)

        # add noise to embedding
        x += torch.randn(x.shape).to(self.options.gpu_id) * self.options.word_embeddings_noise

        if self.options.static:
            x = Variable(x)

        x = x.unsqueeze(1)  # (N, Ci, W, D)

        # first level
        x11 = F.relu(self.conv12(x)).squeeze(3)  # (N, Co, W)
        x12 = F.relu(self.conv13(x)).squeeze(3)  # (N, Co, W)
        x13 = F.relu(self.conv14(x)).squeeze(3)  # (N, Co, W)
        x14 = F.relu(self.conv15(x)).squeeze(3)  # (N, Co, W)
        x15 = F.relu(self.conv16(x)).squeeze(3)  # (N, Co, W)
        x11_out = F.max_pool1d(x11, x11.size(2)).squeeze(2)
        x12_out = F.max_pool1d(x12, x12.size(2)).squeeze(2)
        x13_out = F.max_pool1d(x13, x13.size(2)).squeeze(2)
        x14_out = F.max_pool1d(x14, x14.size(2)).squeeze(2)
        x15_out = F.max_pool1d(x15, x15.size(2)).squeeze(2)

        x = torch.cat((x11_out, x12_out, x13_out, x14_out, x15_out), 1)  # (N,len(Ks)*Co)

        if self.options.n_layers > 1:
            # second level
            x21 = F.max_pool1d(x11, 3).squeeze(2)
            x22 = F.max_pool1d(x12, 3).squeeze(2)
            x23 = F.max_pool1d(x13, 3).squeeze(2)
            x24 = F.max_pool1d(x14, 3).squeeze(2)
            x25 = F.max_pool1d(x15, 3).squeeze(2)
            x21 = F.relu(self.conv22(x21.transpose(1, 2).unsqueeze(1))).squeeze(3)  # (N, Co, W)
            x22 = F.relu(self.conv23(x22.transpose(1, 2).unsqueeze(1))).squeeze(3)  # (N, Co, W)
            x23 = F.relu(self.conv24(x23.transpose(1, 2).unsqueeze(1))).squeeze(3)  # (N, Co, W)
            x24 = F.relu(self.conv25(x24.transpose(1, 2).unsqueeze(1))).squeeze(3)  # (N, Co, W)
            x25 = F.relu(self.conv26(x25.transpose(1, 2).unsqueeze(1))).squeeze(3)  # (N, Co, W)
            x21_out = F.max_pool1d(x21, x21.size(2)).squeeze(2)
            x22_out = F.max_pool1d(x22, x22.size(2)).squeeze(2)
            x23_out = F.max_pool1d(x23, x23.size(2)).squeeze(2)
            x24_out = F.max_pool1d(x24, x24.size(2)).squeeze(2)
            x25_out = F.max_pool1d(x25, x25.size(2)).squeeze(2)
            x = torch.cat((x, x21_out, x22_out, x23_out, x24_out, x25_out), 1)  # (N,len(Ks)*Co)

        self.global_feature_vector = x
        x = self.dropout(self.global_feature_vector)  # (N, len(Ks)*Co)

        return self.fc(x)
