# Leveraging AI Predicted and Expert Revised Annotations in Interactive Segmentation: Continual Tuning or Full Training?

<p align="center"><img width="100%" src="documents/Our_Structure.png" /></p>

## Paper

<b>Leveraging AI Predicted and Expert Revised Annotations in Interactive Segmentation: Continual Tuning or Full Training?</b> <br/>
[Tiezheng Zhang](https://github.com/ollie-ztz)<sup>1</sup>, [Xiaoxi Chen](https://github.com/skbtskbt)<sup>2</sup>, [Chongyu Qu](https://github.com/Chongyu1117)<sup>1</sup>, [Alan L. Yuille](https://www.cs.jhu.edu/~ayuille/)<sup>1</sup>, and [Zongwei Zhou](https://www.zongweiz.com/)<sup>1,*</sup> <br/>
<sup>1 </sup>Johns Hopkins University,  <br/>
<sup>2 </sup>Shanghai Jiao Tong University  <br/>
ISBI 2024 <br/>
[paper](https://arxiv.org/pdf/2402.19423.pdf) | [code](https://github.com/ollie-ztz/Continue_Tuning) | [poster](Coming Soon)

<b>RSNA 2023 (Oral Presentation)</b><br/>
[paper](documents/RSNA2023.pdf) | [code](https://github.com/ollie-ztz/Continue_Tuning) | [slides](documents/RSNA_Poster.pdf)


## 0. Installation

```bash
git clone https://github.com/ollie-ztz/Continue_Tuning
```

See [installation instructions](document/INSTALL.md) to create an environment and obtain requirements.

## 1. Download AI models

We offer pre-trained checkpoints of Swin UNETR and U-Net. The models were trained on a combination of 14 publicly available CT datasets, consisting of 3,410 (see details in [CLIP-Driven Universal Model](https://github.com/ljwztc/CLIP-Driven-Universal-Model)).
Download the trained models and save them into `./pretrained_checkpoints/`.

| Architecture | Param | Download |
|  ----  | ----  |  ----  |
| U-Net  | 19.08M | [link](https://www.dropbox.com/s/lyunaue0wwhmv5w/unet.pth) |
| Swin UNETR | 62.19M | [link](https://www.dropbox.com/s/jdsodw2vemsy8sz/swinunetr.pth) |

## 2. Prepare your datasets

Our method could be applied to publicly available datasets (e.g.m BTCV) or your private datasets. For the public datasets, please refer to [CLIP-Driven Universal Model](https://github.com/ljwztc/CLIP-Driven-Universal-Model). Currently, we only take data formatted in `nii.gz`. 

##### 2.1 Preparing

Taking the BTCV dataset as an example, prepare your datasets as shown below.
```bash
01_Multi-Atlas_Labeling/img/img0002.nii.gz	01_Multi-Atlas_Labeling/label/label0002.nii.gz
```

##### 2.2 Preprocessing

Generate a list for this dataset.

```bash
cd AbdomenAtlas/
python -W ignore generate_datalist.py --data_path $datapath --dataset_name $dataname --folder img --out ./dataset/dataset_list --save_file $dataname.txt
```

## 3. Generate masks

##### U-Net
```bash
CUDA_VISIBLE_DEVICES=0 python -W ignore test.py --resume pretrained_checkpoints/unet.pth --backbone unet --save_dir $savepath --dataset_list $dataname --data_root_path $datapath --store_result >> logs/$dataname.unet.txt
```

##### Swin UNETR
```bash
CUDA_VISIBLE_DEVICES=0 python -W ignore test.py --resume pretrained_checkpoints/swinunetr.pth --backbone swinunetr --save_dir $savepath --dataset_list $dataname --data_root_path $datapath --store_result >> logs/$dataname.swinunetr.txt
```
To generate attention maps for the active learning process (Step 5 [optional]), remember to save entropy and soft predictions by using the options `--store_entropy` and `--store_soft_pred`



<!-- ## Citation 

```
@article{qu2024abdomenatlas,
  title={Abdomenatlas-8k: Annotating 8,000 CT volumes for multi-organ segmentation in three weeks},
  author={Qu, Chongyu and Zhang, Tiezheng and Qiao, Hualin and Tang, Yucheng and Yuille, Alan L and Zhou, Zongwei and others},
  journal={Advances in Neural Information Processing Systems},
  volume={36},
  year={2023}
}
``` -->

## Acknowledgements
This work was supported by the Lustgarten Foundation for Pancreatic Cancer Research and partially by the Patrick J. McGovern Foundation Award. We appreciate the effort of the MONAI Team to provide open-source code for the community.
