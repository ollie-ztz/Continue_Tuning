# Installation
### Create Environments
```bash
conda create -n ConT python=3.9
source activate ConT
cd Continue_Tuning/
pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
pip install monai[all]==0.9.0
pip install -r requirements.txt
```

### Download Pretrained Weights

```bash
cd pretrained_weights/
wget https://www.dropbox.com/s/po2zvqylwr0fuek/swin_unetr.base_5000ep_f48_lr2e-4_pretrained.pt
wget https://www.dropbox.com/s/lh5kuyjxwjsxjpl/Genesis_Chest_CT.pt
cd ../
cd pretrained_checkpoints/
wget https://www.dropbox.com/s/jdsodw2vemsy8sz/swinunetr.pth
wget https://www.dropbox.com/s/lyunaue0wwhmv5w/unet.pth
cd ..
```

<!-- ### Define Variables

```bash
dataname=01_Multi-Atlas_Labeling # an example
datapath=/medical_backup/PublicAbdominalData/
savepath=/medical_backup/Users/zzhou82/outs
``` -->