import torch
from model import Classifier

checkpoint = torch.load('checkpoints/latest.pth.tar')
model = Classifier()
model.eval()

model.load_state_dict(checkpoint['model_state']['state_dict'])
model.cpu()

torch.save(model.state_dict(), 'checkpoints/production.tar')