# Leveraging AI Predicted and Expert Revised Annotations in Interactive Segmentation: Continual Tuning or Full Training?

Interactive segmentation, an integration of AI algorithms and human expertise, premises to improve the accuracy and efficiency of curating large-scale, detailed-annotated datasets in healthcare. Human experts revise the annotations predicted by AI, and in turn, AI improves its predictions by learning from these revised annotations. This interactive process continues to enhance the quality of annotations until no major revision is needed from experts. The key challenge is how to leverage **AI predicted** and **expert revised** annotations to iteratively improve the AI. Two problems arise: (1) The risk of catastrophic forgetting---the AI tends to forget the previously learned classes if it is only retrained using the expert revised classes. (2) Computational inefficiency when retraining the AI using both AI predicted and expert revised annotations; moreover, given the dominant AI predicted annotations in the dataset, the contribution of newly revised annotations---often account for a very small fraction---to the AI training remains marginal. This paper proposes **Continual Tuning** to address the problems from two perspectives: network design and data reuse. Firstly, we design a shared network for all classes followed by class-specific networks dedicated to individual classes. To mitigate forgetting, we freeze the shared network for previously learned classes and only update the class-specific network for revised classes. Secondly, we reuse a small fraction of data with previous annotations to avoid over-computing. The selection of such data relies on the importance estimate of each data. The importance score is computed by combining the uncertainty and consistency of AI predictions. Our experiments demonstrate that Continual Tuning achieves a speed **16 times** greater than repeatedly training AI from scratch without compromising the performance.

## Paper

<b>Leveraging AI Predicted and Expert Revised Annotations in Interactive Segmentation: Continual Tuning or Full Training?</b> <br/>
[Tiezheng Zhang](https://github.com/ollie-ztz)<sup>1</sup>, [Xiaoxi Chen](https://github.com/skbtskbt)<sup>2</sup>, [Chongyu Qu](https://github.com/Chongyu1117)<sup>1</sup>, [Alan L. Yuille](https://www.cs.jhu.edu/~ayuille/)<sup>1</sup>, and [Zongwei Zhou](https://www.zongweiz.com/)<sup>1,*</sup> <br/>
<sup>1 </sup>Johns Hopkins University,  <br/>
<sup>2 </sup>Shanghai Jiao Tong University  <br/>
ISBI 2024 <br/>
[paper](Coming Soon) | [code](https://github.com/ollie-ztz/Continue_Tuning) | [poster](Coming Soon)

<!-- <b>AbdomenAtlas-8K: Human-in-the-Loop Annotating Eight Anatomical Structures for 8,448 Three-Dimensional Computed Tomography Volumes in Three Weeks</b> <br/>
[Chongyu Qu](https://github.com/Chongyu1117)<sup>1</sup>, [Tiezheng Zhang](https://github.com/ollie-ztz)<sup>1</sup>, [Hualin Qiao](https://www.linkedin.com/in/hualin-qiao-a29438210/)<sup>2</sup>, [Jie Liu](https://ljwztc.github.io/)<sup>3</sup>, [Yucheng Tang](https://scholar.google.com/citations?hl=en&user=0xheliUAAAAJ)<sup>4</sup>, [Alan L. Yuille](https://www.cs.jhu.edu/~ayuille/)<sup>1</sup>, and [Zongwei Zhou](https://www.zongweiz.com/)<sup>1,*</sup> <br/>
<sup>1 </sup>Johns Hopkins University,  <br/>
<sup>2 </sup>Rutgers University,  <br/>
<sup>3 </sup>City University of Hong Kong,   <br/>
<sup>4 </sup>NVIDIA <br/> -->
<b>RSNA 2023 (Oral Presentation) <br/>
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

It can be publicly available datasets (e.g., BTCV) or your private datasets. Currently, we only take data formatted in `nii.gz`. This repository will help you assign annotations to these datasets, including 25 organs and six types of tumors (*where the annotation of eight organs is pretty accurate*).

##### 2.1 Download

Taking the BTCV dataset as an example, download this dataset and save it to the `datapath` directory.
```bash
cd $datapath
wget https://www.dropbox.com/s/jnv74utwh99ikus/01_Multi-Atlas_Labeling.tar.gz
tar -xzvf 01_Multi-Atlas_Labeling.tar.gz
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

## 4. Data Assembly

In the assembly process, our utmost priority is given to the original annotations supplied by each public dataset. Subsequently, we assign secondary priority to the revised labels from our annotators. The pseudo labels, generated by AI models, are accorded the lowest priority. The following code can implement this priority into the assembled dataset.

```bash
python -W ignore assemble.py --data_path $savepath --dataset_name $dataname --backbone swinunetr --save_dir SAVE_DIR --version V1
```

This is how our AbdonmenAtlas-8K appears
```
    $savepath/
    ├── $dataname_img0001
    ├── $dataname_img0002
    ├── $dataname_img0003
        │── ct.nii.gz
        ├── original_label.nii.gz
        ├── pseudo_label.nii.gz
        └── segmentations
            ├── spleen.nii.gz
            ├── liver.nii.gz
            ├── pancreas.nii.gz
```


<!-- ## TODO

- [x] Release pre-trained AI model checkpoints (U-Net and Swin UNETR)
- [x] Release the AbdomenAtlas-8K dataset (we commit to releasing 3,410 of the 8,448 CT volumes)
- [ ] Support more data formats (e.g., dicom) -->

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