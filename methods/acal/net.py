import torch.nn as nn
from torch.nn import functional as F


class Classifier(nn.Module):
    def __init__(self, n_class, n_ch, ncf):
        super(Classifier, self).__init__()
        self.res = 32
        self.conv1 = nn.Conv2d(n_ch, 20, 5)
        self.conv2 = nn.Conv2d(20, 50, 5)
        self.fc_input_len = (((self.res - 4) // 2 - 4) // 2) ** 2 * 50
        self.fc1 = nn.Linear(self.fc_input_len, ncf)
        self.fc2 = nn.Linear(ncf, n_class)
        self.drop = nn.Dropout()

    def __call__(self, x):
        h = F.max_pool2d(F.relu(self.conv1(x)), 2, stride=2)
        h = F.max_pool2d(F.relu(self.conv2(h)), 2, stride=2)
        h = self.drop(F.relu(self.fc1(h.view(x.size(0), -1))))
        return self.fc2(h)

# classifier in DANN + BN
# class Classifier(nn.Module):
#     def __init__(self):
#         super(Classifier, self).__init__()
#         self.conv1 = nn.Conv2d(3, 64, kernel_size=5, stride=1, padding=2)
#         self.bn1 = nn.BatchNorm2d(64)
#         self.conv2 = nn.Conv2d(64, 64, kernel_size=5, stride=1, padding=2)
#         self.bn2 = nn.BatchNorm2d(64)
#         self.conv3 = nn.Conv2d(64, 128, kernel_size=5, stride=1, padding=2)
#         self.bn3 = nn.BatchNorm2d(128)
#         self.fc1 = nn.Linear(8192, 3072)
#         self.bn1_fc = nn.BatchNorm1d(3072)
#         self.fc2 = nn.Linear(3072, 2048)
#         self.bn2_fc = nn.BatchNorm1d(2048)
#         self.fc3 = nn.Linear(2048, 10)
#         self.dropout = nn.Dropout(0.5)
#
#     def forward(self, x):
#         x = F.max_pool2d(F.relu(self.bn1(self.conv1(x))), stride=2,
#                          kernel_size=3, padding=1)
#         x = F.max_pool2d(F.relu(self.bn2(self.conv2(x))), stride=2,
#                          kernel_size=3, padding=1)
#         x = F.relu(self.bn3(self.conv3(x)))
#         x = x.view(x.size(0), 8192)
#         x = self.dropout(F.relu(self.bn1_fc(self.fc1(x))))
#         x = self.dropout(F.relu(self.bn2_fc(self.fc2(x))))
#         x = self.fc3(x)
#         return x

# class Classifier(nn.Module):
#     def __init__(self, n_class, n_ch):
#         super(Classifier, self).__init__()
#         self.res = 32
#         self.conv1 = nn.Conv2d(n_ch, 20, 5)
#         self.conv2 = nn.Conv2d(20, 50, 5)
#         self.fc_input_len = (((self.res - 4) // 2 - 4) // 2) ** 2 * 50
#         self.fc1 = nn.Linear(self.fc_input_len, 50)
#         self.fc2 = nn.Linear(50, 10)
#         self.fc3 = nn.Linear(10, n_class)
#         self.drop = nn.Dropout()
#
#     def __call__(self, x):
#         h = F.max_pool2d(F.relu(self.conv1(x)), 2, stride=2)
#         h = F.max_pool2d(F.relu(self.conv2(h)), 2, stride=2)
#         h = self.drop(F.relu(self.fc1(h.view(x.size(0), -1))))
#         h = self.drop(F.relu(self.fc2(h)))
#         return self.fc3(h)

# This newtork is used in various previous baselines for 32x32 input
# class Classifier(nn.Module):
#     def __init__(self, n_class, n_ch=3, use_drop=True):
#         super(Classifier, self).__init__()
#         self.conv1 = nn.Conv2d(n_ch, 64, 5, padding=2)
#         self.conv2 = nn.Conv2d(64, 64, 5, padding=2)
#         self.conv3 = nn.Conv2d(64, 128, 5, padding=2)
#         self.fc1 = nn.Linear(((32 // 4) ** 2) * 128, 3072)
#         self.fc2 = nn.Linear(3072, 2048)
#         self.fc3 = nn.Linear(2048, n_class)
#         self.drop = nn.Dropout() if use_drop else None
#
#     def __call__(self, x):
#         h = F.max_pool2d(F.relu(self.conv1(x)), 3, stride=2, padding=1)
#         h = F.max_pool2d(F.relu(self.conv2(h)), 3, stride=2, padding=1)
#         h = F.relu(self.conv3(h))
#         h = F.relu(self.fc1(h.view(x.size(0), -1)))
#         if self.drop: h = self.drop(h)
#         h = F.relu(self.fc2(h))
#         if self.drop: h = self.drop(h)
#         return self.fc3(h)
