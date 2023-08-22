import os
import numpy as np
from tqdm import tqdm
# I want to store the files which in their 'segmentations' folder, there are files end with 'V1.nii.gz'

# path = '/mnt/tzhang85/AbdomenAtlas_8K_internal'
path = '/mnt/tiezheng/continue_learning_data/08_AbdomenCT-1K_200_400/08_AbdomenCT-1K'
dataset_name = '08_AbdomenCT-1K'
# backbone = 'swinunetr_onehot'
# organs = ['liver','kidney_right','spleen','pancreas','aorta','postcava',
#                        'adrenal_gland_right','adrenal_gland_left','gall_bladder','stomach','duodenum','kidney_left','colon']
# organs_set = {'aorta':1,'adrenal_gland_right':2,'adrenal_gland_left':2,'colon':6,'duodenum':7,'gall_bladder':8,'postcava':9,
#                     'kidney_left':10,'kidney_right':11,'liver':12,'pancreas':13,'spleen':18,'stomach':19}
res = []
file_list = os.listdir(path)
for files in tqdm(file_list):
    if files.startswith('Case'):
        segs = os.listdir(os.path.join(path,files,'average','segmentations'))
        for seg in segs:
            if seg.endswith('revised.nii.gz'):
                res.append(files)
# store the res into a txt file
with open('R2_list.txt','w') as file:
    for item in res:
        file.write(item+'\n')
