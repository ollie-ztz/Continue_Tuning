import torch
from torch import nn
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import argparse
import time

import warnings
warnings.filterwarnings("ignore")

import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel
from tensorboardX import SummaryWriter

from model.Universal_model import Universal_model
from dataset.dataloader import get_loader
from utils import loss
from utils.utils import TEMPLATE, get_key, merge_organ, containing_totemplate
from optimizers.lr_scheduler import LinearWarmupCosineAnnealingLR


torch.multiprocessing.set_sharing_strategy('file_system')


            

def train(args, train_loader, model, optimizer, loss_seg_DICE, loss_seg_CE):
    model.train()
    loss_bce_ave = 0
    loss_dice_ave = 0
    epoch_iterator = tqdm(
        train_loader, desc="Training (X / X Steps) (loss=X.X)", dynamic_ncols=True
    )
    for step, batch in enumerate(epoch_iterator):
        # Assuming we use our pseudo label here to train and we only care about the original 5 organs for dataset 08
        x, lbl, name = batch["image"].to(args.device), batch["label"].float(), batch['name']
        B, C, W, H, D = lbl.shape
        y = torch.zeros(B,args.NUM_CLASS,W,H,D)
        for b in range(B):
            for src,tgt in enumerate(TEMPLATE['all']):
                y[b][src][lbl[b][0]==tgt] = 1
        if args.original_label:
            for b in range(B):
                for c in range(args.NUM_CLASS):
                    if c+1 not in TEMPLATE['finetune_com']:
                        y[b][c] = 0
        y = merge_organ(args,y,containing_totemplate)
        y = y.to(args.device)
        logit_map = model(x)
        term_seg_Dice = loss_seg_DICE.forward(logit_map, y, name, TEMPLATE)
        term_seg_BCE = loss_seg_CE.forward(logit_map, y, name, TEMPLATE)
        loss = term_seg_BCE + term_seg_Dice
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()
        epoch_iterator.set_description(
            "Epoch=%d: Training (%d / %d Steps) (dice_loss=%2.5f, bce_loss=%2.5f)" % (
                args.epoch, step, len(train_loader), term_seg_Dice.item(), term_seg_BCE.item())
        )
        loss_bce_ave += term_seg_BCE.item()
        loss_dice_ave += term_seg_Dice.item()
        torch.cuda.empty_cache()
    print('Epoch=%d: ave_dice_loss=%2.5f, ave_bce_loss=%2.5f' % (args.epoch, loss_dice_ave/len(epoch_iterator), loss_bce_ave/len(epoch_iterator)))
    
    return loss_dice_ave/len(epoch_iterator), loss_bce_ave/len(epoch_iterator)

def process(args):
    rank = 0
    if args.dist:
        dist.init_process_group(backend="nccl", init_method="env://")
        rank = args.local_rank
    args.device = torch.device(f"cuda:{rank}")
    torch.cuda.set_device(args.device)

    # prepare the 3D model
    model = Universal_model(img_size=(args.roi_x, args.roi_y, args.roi_z),
                    in_channels=1,
                    out_channels=args.NUM_CLASS,
                    backbone=args.backbone,
                    encoding=args.trans_encoding
                    )
    # define the non-frozen-layers
    if args.continual_tuning:
        layers_to_not_frozen = ['controllers.3.0.weight','controllers.3.0.bias','controllers.3.2.weight','controllers.3.2.bias',
                                'controllers.6.0.weight','controllers.6.0.bias','controllers.6.2.weight','controllers.6.2.bias',
                                'controllers.7.0.weight','controllers.7.0.bias','controllers.7.2.weight','controllers.7.2.bias',
                                'controllers.8.0.weight','controllers.8.0.bias','controllers.8.2.weight','controllers.8.2.bias'  
                                ]
        for name, param in model.named_parameters():
            if any(layer in name for layer in layers_to_not_frozen):
                param.requires_grad = True
            else:
                param.requires_grad = False

    #Load pre-trained weights
    if args.pretrain is not None:
        model.load_params(torch.load(args.pretrain)["state_dict"])

    if args.trans_encoding == 'word_embedding':
        word_embedding = torch.load(args.word_embedding)
        model.organ_embedding.data = word_embedding.float()
        print('load word embedding')

    model.to(args.device)
    model.train()
    if args.dist:
        model = DistributedDataParallel(model, device_ids=[args.device])

    # criterion and optimizer
    loss_seg_DICE = loss.DiceLoss(num_classes=args.NUM_CLASS).to(args.device)
    loss_seg_CE = loss.Multi_BCELoss(num_classes=args.NUM_CLASS).to(args.device)
    if args.continual_tuning:
        optimizer = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=args.lr, weight_decay=args.weight_decay)
    else:
        optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    scheduler = LinearWarmupCosineAnnealingLR(optimizer, warmup_epochs=args.warmup_epoch, max_epochs=args.max_epoch)


    #Load pre-trained weights
    store_dict = model.state_dict()
    store_dict_keys = [key for key, value in store_dict.items()]

    if args.resume:
        checkpoint = torch.load(args.resume)
        # added for resume
        load_dict = checkpoint['net']
        load_dict_value = [value for key, value in load_dict.items()]
        for i in range(len(store_dict)):
            store_dict[store_dict_keys[i]] = load_dict_value[i]
        model.load_state_dict(store_dict)
            
        # #Becareful, the optimizer should be loaded after the model
        # optimizer.load_state_dict(checkpoint['optimizer'])
        args.epoch = checkpoint['epoch']
        # scheduler.load_state_dict(checkpoint['scheduler'])
        
        print('success resume from ', args.resume)

    torch.backends.cudnn.benchmark = True

    train_loader, train_sampler = get_loader(args)

    if rank == 0:
        writer = SummaryWriter(log_dir='out/' + args.log_name)
        print('Writing Tensorboard logs to ', 'out/' + args.log_name)

    while args.epoch < args.max_epoch:
        if args.dist:
            dist.barrier()
            train_sampler.set_epoch(args.epoch)
        scheduler.step()

        loss_dice, loss_bce = train(args, train_loader, model, optimizer, loss_seg_DICE, loss_seg_CE)
        if rank == 0:
            writer.add_scalar('train_dice_loss', loss_dice, args.epoch)
            writer.add_scalar('train_bce_loss', loss_bce, args.epoch)
            writer.add_scalar('lr', scheduler.get_lr(), args.epoch)

        if (args.epoch % args.store_num == 0 and args.epoch != 0) and rank == 0:
            checkpoint = {
                "net": model.state_dict(),
                'optimizer':optimizer.state_dict(),
                'scheduler': scheduler.state_dict(),
                "epoch": args.epoch
            }
            if not os.path.isdir('out/' + args.log_name):
                os.mkdir('out/' + args.log_name)
            torch.save(checkpoint, 'out/' + args.log_name + '/epoch_' + str(args.epoch) + '.pth')
            print('save model success')

        args.epoch += 1

    dist.destroy_process_group()

def main():
    parser = argparse.ArgumentParser()
    ## for distributed training
    parser.add_argument('--dist', dest='dist', type=bool, default=False,
                        help='distributed training or not')
    parser.add_argument("--local_rank", type=int)
    parser.add_argument("--device")
    parser.add_argument("--epoch", default=0)
    ## logging
    parser.add_argument('--log_name', default='swinunetr', help='The path resume from checkpoint')
    ## model load
    parser.add_argument('--backbone', default='swinunetr', help='backbone [swinunetr or unet or dints or unetpp,swinunetr_onehot]')
    parser.add_argument('--resume', default=None, help='The path resume from checkpoint')
    parser.add_argument('--pretrain', default=None,
                        help='The path of pretrain model. Eg, ./pretrained_weights/swin_unetr.base_5000ep_f48_lr2e-4_pretrained.pt')
    parser.add_argument('--trans_encoding', default='word_embedding', 
                        help='the type of encoding: rand_embedding or word_embedding')
    parser.add_argument('--word_embedding', default='./pretrained_weights/txt_encoding.pth', 
                        help='The path of word embedding')
    ## hyperparameter
    parser.add_argument('--max_epoch', default=1000, type=int, help='Number of training epoches')
    parser.add_argument('--store_num', default=50, type=int, help='Store model how often')
    parser.add_argument('--warmup_epoch', default=20, type=int, help='number of warmup epochs')
    parser.add_argument('--lr', default=1e-4, type=float, help='Learning rate')
    parser.add_argument('--weight_decay', default=1e-5, help='Weight Decay')
    ## dataset
    parser.add_argument('--dataset_list', nargs='+', default=['PAOT_123457891213', 'PAOT_10_inner']) # 'PAOT', 'felix'
    parser.add_argument('--data_root_path', default='/computenodes/node31/team1/jliu/data/ct_data/', help='data root path')
    parser.add_argument('--data_txt_path', default='./dataset/dataset_list/', help='data txt path')
    parser.add_argument('--batch_size', default=4, type=int,help='batch size')
    parser.add_argument('--num_workers', default=8, type=int, help='workers numebr for DataLoader')
    parser.add_argument('--a_min', default=-175, type=float, help='a_min in ScaleIntensityRanged')
    parser.add_argument('--a_max', default=250, type=float, help='a_max in ScaleIntensityRanged')
    parser.add_argument('--b_min', default=0.0, type=float, help='b_min in ScaleIntensityRanged')
    parser.add_argument('--b_max', default=1.0, type=float, help='b_max in ScaleIntensityRanged')
    parser.add_argument('--space_x', default=1.5, type=float, help='spacing in x direction')
    parser.add_argument('--space_y', default=1.5, type=float, help='spacing in y direction')
    parser.add_argument('--space_z', default=1.5, type=float, help='spacing in z direction')
    parser.add_argument('--roi_x', default=96, type=int, help='roi size in x direction')
    parser.add_argument('--roi_y', default=96, type=int, help='roi size in y direction')
    parser.add_argument('--roi_z', default=96, type=int, help='roi size in z direction')
    parser.add_argument('--num_samples', default=2, type=int, help='sample number in each ct')
    parser.add_argument('--NUM_CLASS', default=8, type=int, help='number of labels')

    parser.add_argument('--phase', default='train', help='train or validation or test')
    parser.add_argument('--uniform_sample', action="store_true", default=False, help='whether utilize uniform sample strategy')
    parser.add_argument('--datasetkey', nargs='+', default=['01', '02', '03', '04', '05', 
                                            '07', '08', '09', '12', '13', '10_03', 
                                            '10_06', '10_07', '10_08', '10_09', '10_10','18'],
                                            help='the content for ')
    parser.add_argument('--cache_dataset', action="store_true", default=False, help='whether use cache dataset')
    parser.add_argument('--cache_rate', default=0.005, type=float, help='The percentage of cached data in total')
    parser.add_argument('--internal_organ', default=True , type=bool, help='Ourdata or internal organ')
    parser.add_argument('--original_label',action="store_true",default=False,help='whether use original label')
    parser.add_argument('--continual_tuning',action="store_true",default=False,help='whether use freeze')


    args = parser.parse_args()
    
    process(args=args)

if __name__ == "__main__":
    main()