# -*- coding: utf-8 -*-
"""Untitled20.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1F45-Th1RsfdSAE8EwGIsYtu3wm1h6-lO
"""

import numpy as np
import torch
from torch import nn
from torch.utils.data import Dataset

class SiameseDataset(Dataset):

  def __init__(self, x, y, transform = None):
    self.x = x
    self.transform = transform
    self.y = y.reshape(-1)

  def __getitem__(self, idx):
    anchor = self.x[idx]
    same_class_idx = np.arange(self.x.shape[0])[idx//20 * 20 : (idx//20 + 1) * 20]
    other_class_idx = np.concatenate((np.arange(self.x.shape[0])[0 : idx//20 * 20],
                                      np.arange(self.x.shape[0])[(idx//20 + 1) * 20 :]))


    positive = self.x[np.random.choice(same_class_idx)]
    positive = positive + self.x[np.random.choice(other_class_idx)] + self.x[np.random.choice(other_class_idx)]

    negative = self.x[np.random.choice(other_class_idx)]
    negative = negative + self.x[np.random.choice(other_class_idx)] + self.x[np.random.choice(other_class_idx)]
    if self.transform is not None:
      anchor = self.transform(anchor)
      positive = self.transform(positive)
      negative = self.transform(negative)
    return anchor, positive, negative


  def __len__(self):
    return len(self.x)

class ValidationSiameseDataset(Dataset):

  def __init__(self, x, y, transform):
    self.x = x
    self.transform = transform
    self.y = y.reshape(-1)

  def __getitem__(self, idx):
    anchor = self.x[idx]
    same_class_idx = np.arange(self.x.shape[0])[idx//5 * 5 : (idx//5 + 1) * 5]
    other_class_idx = np.concatenate((np.arange(self.x.shape[0])[0 : idx//5 * 5],
                                      np.arange(self.x.shape[0])[(idx//5 + 1) * 5 :]))

    positive = self.x[np.random.choice(same_class_idx)]
    positive = positive + self.x[np.random.choice(other_class_idx)] + self.x[np.random.choice(other_class_idx)]

    negative = self.x[np.random.choice(other_class_idx)]
    negative = negative + self.x[np.random.choice(other_class_idx)] + self.x[np.random.choice(other_class_idx)]

    if self.transform is not None:
      anchor = self.transform(anchor)
      positive = self.transform(positive)
      negative = self.transform(negative)
    return anchor, positive, negative



  def __len__(self):
    return len(self.x)

class SiameseNet(nn.Module):

    def __init__(self, latent_dim):
      super().__init__()
      self.latent_dim = latent_dim
      self.model = nn.Sequential(nn.Conv1d(in_channels=1, out_channels=16,kernel_size=21, padding = 'same'),
                                  nn.MaxPool1d(kernel_size=2, stride=2),
                                  nn.LeakyReLU(),
                                  nn.BatchNorm1d(16),
                                  nn.Conv1d(16, 32, 11, padding = 'same'),
                                  nn.MaxPool1d(2, 2),
                                  nn.LeakyReLU(),
                                  nn.BatchNorm1d(32),
                                  nn.Conv1d(32, 64, 5, padding = 'same'),
                                  nn.MaxPool1d(2, 2),
                                  nn.LeakyReLU(),
                                  nn.BatchNorm1d(64),

                                 nn.Flatten(),
                                 nn.Linear(64*625, self.latent_dim))


    def _forward(self, x):
      out = x.view(-1, 1, 5000)
      out = self.model(out)
      # normalize embedding to unit vector
      out = torch.nn.functional.normalize(out)
      return out


    def predict(self, x):
      out = x.view(-1, 1, 5000)
      out = self.model(out)
      out = torch.nn.functional.normalize(out)
      return out

    def forward(self, anchor, positive, negative, latent_dim):
        output1 = self._forward(anchor)
        output2 = self._forward(positive)
        output3 = self._forward(negative)

        return output1, output2, output3

class TripletLoss(nn.Module):
    """
    Triplet loss
    Takes embeddings of an anchor sample, a positive sample and a negative sample
    """

    def __init__(self, margin, semi_hard):
        super(TripletLoss, self).__init__()
        self.margin = margin
        self.semi_hard = semi_hard

    def forward(self, anchor, positive, negative, size_average=True):
        distance_positive = 1.0 - F.cosine_similarity(anchor, positive)
        distance_negative = 1.0 - F.cosine_similarity(anchor, negative)
        losses = F.relu(distance_positive - distance_negative + self.margin)
        losses = torch.where(losses > self.semi_hard, losses, torch.zeros(losses.shape).to(device))
        return losses.sum()/torch.count_nonzero(losses) if size_average else losses.sum(), torch.count_nonzero(losses)
