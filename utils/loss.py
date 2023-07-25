import torch
import torch.nn.functional as F
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import scipy.ndimage as nd
from matplotlib import pyplot as plt
from torch import Tensor, einsum


class BinaryDiceLoss(nn.Module):
    def __init__(self, smooth=1, p=2, reduction='mean'):
        super(BinaryDiceLoss, self).__init__()
        self.smooth = smooth
        self.p = p
        self.reduction = reduction

    def forward(self, predict, target):
        assert predict.shape[0] == target.shape[0], "predict & target batch size don't match"
        predict = predict.contiguous().view(predict.shape[0], -1)
        target = target.contiguous().view(target.shape[0], -1)

        num = torch.sum(torch.mul(predict, target), dim=1)
        den = torch.sum(predict, dim=1) + torch.sum(target, dim=1) + self.smooth

        dice_score = 2*num / den
        dice_loss = 1 - dice_score

        dice_loss_avg = dice_loss[target[:,0]!=-1].sum() / dice_loss[target[:,0]!=-1].shape[0]

        return dice_loss_avg

class DiceLoss(nn.Module):
    def __init__(self, weight=None, ignore_index=None, num_classes=3, **kwargs):
        super(DiceLoss, self).__init__()
        self.kwargs = kwargs
        self.weight = weight
        self.ignore_index = ignore_index
        self.num_classes = num_classes
        self.dice = BinaryDiceLoss(**self.kwargs)

    def forward(self, predict, target, name, TEMPLATE):

        predict = F.sigmoid(predict)

        total_loss = []
        B = predict.shape[0]
        for b in range(B):
            target_sum = torch.sum(target[b],axis = (1,2,3))
            assert len(target_sum) == 32, 'target sum =! 32'
            non_zero_tensor = torch.nonzero(target_sum).squeeze()
            non_zero_list = non_zero_tensor.tolist() if non_zero_tensor.dim() > 0 else [non_zero_tensor.tolist()]
            # for all
            # organ_list = TEMPLATE['all']
            # for part
            organ_list = TEMPLATE['all']
            new_list = []
            for idx in non_zero_list:
                if idx+1 in organ_list:
                    new_list.append(idx+1)
            if len(new_list)!=0:     
                for organ in new_list:
                    dice_loss = self.dice(predict[b, organ-1], target[b, organ-1])
                    total_loss.append(dice_loss)
            if len(total_loss) == 0:
                return torch.tensor(1.0).cuda()
        total_loss = torch.stack(total_loss)
        return total_loss.sum()/total_loss.shape[0]


class Multi_BCELoss(nn.Module):
    def __init__(self, ignore_index=None, num_classes=3, **kwargs):
        super(Multi_BCELoss, self).__init__()
        self.kwargs = kwargs
        self.num_classes = num_classes
        self.ignore_index = ignore_index
        self.criterion = nn.BCEWithLogitsLoss()

    def forward(self, predict, target, name, TEMPLATE):
        assert predict.shape[2:] == target.shape[2:], 'predict & target shape do not match'

        total_loss = []
        B = predict.shape[0]
        for b in range(B):
            organ_list = TEMPLATE['all']
            for organ in organ_list:
                ce_loss = self.criterion(predict[b, organ-1], target[b, organ-1])
                total_loss.append(ce_loss)
        total_loss = torch.stack(total_loss)

        return total_loss.sum()/total_loss.shape[0]
