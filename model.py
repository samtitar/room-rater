import torch.nn as nn
import torch.nn.functional as F

class Classifier(nn.Module):
    def __init__(self):
        super(Classifier, self).__init__()
        self.convolve = nn.Sequential(
            # 256x256 to 64x64
            nn.Conv2d(3, 32, kernel_size=4, stride=4),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),

            # 64x64 to 16x16
            nn.Conv2d(32, 64, kernel_size=4, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            
            # 16x16 to 4x4
            nn.Conv2d(64, 128, kernel_size=4, stride=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
        )

        self.linear = nn.Sequential(
            # Fully connected
            nn.Linear(38016, 1024),
            nn.Linear(1024, 512),
            nn.Linear(512, 128),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.convolve(x)
        print(x.shape)
        return self.linear(x)
