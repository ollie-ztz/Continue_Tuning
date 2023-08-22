# import os
# import numpy as np
# from tqdm import tqdm
# import shutil
# # I want to store the files which in their 'segmentations' folder, there are files end with 'V1.nii.gz'
# # /mnt/tzhang85/AbdomenAtlas_8K_internal/08_AbdomenCT-1K_Case_00297_0000/segmentations
# des_path = '/mnt/tzhang85/AbdomenAtlas_8K_internal'
# src_path = '/mnt/tiezheng/continue_learning_data/08_AbdomenCT-1K_200_400/08_AbdomenCT-1K'
# dataset_name = '08_AbdomenCT-1K'
# # backbone = 'swinunetr_onehot'
# # organs = ['liver','kidney_right','spleen','pancreas','aorta','postcava',
# #                        'adrenal_gland_right','adrenal_gland_left','gall_bladder','stomach','duodenum','kidney_left','colon']
# # organs_set = {'aorta':1,'adrenal_gland_right':2,'adrenal_gland_left':2,'colon':6,'duodenum':7,'gall_bladder':8,'postcava':9,
# #                     'kidney_left':10,'kidney_right':11,'liver':12,'pancreas':13,'spleen':18,'stomach':19}
# res = []
# file_list = os.listdir(src_path)
# for files in tqdm(file_list):
#     if files.startswith('Case'):
#         segs = os.listdir(os.path.join(src_path,files,'average','segmentations'))
#         for seg in segs:
#             if seg.endswith('revised.nii.gz'):
#                 # copy the file to the destination
#                 organ = seg[:-15]
#                 # rename the file in the destination
#                 shutil.copy(os.path.join(des_path,dataset_name+'_'+files,'segmentations',seg[:-15]+'.nii.gz'),os.path.join(des_path,dataset_name+'_'+files,'segmentations',seg[:-15]+'_V1.nii.gz'))
#                 shutil.copy(os.path.join(src_path,files,'average','segmentations',seg),os.path.join(des_path,dataset_name+'_'+files,'segmentations',seg[:-15]+'.nii.gz'))

import numpy as np
import nibabel as nib
import os
from tqdm import tqdm

# Replace the label in pseudo_label.nii.gz if the organ in segmentations has revised version
res =[]
path = '/ccvl/net/ccvl15/tzhang85/AbdomenAtlas_8K_internal'
dataset_name = '08_AbdomenCT-1K'
files_list = os.listdir(path)
for file in tqdm(files_list):
    if file.startswith(dataset_name):
        segs = os.listdir(os.path.join(path,file,'segmentations'))
        for seg in segs:
            if seg.endswith('V1.nii.gz'):
                res.append(file)
res = np.unique(res)
# Replace the label in pseudo_label.nii.gz if the organ in segmentations has revised version with the help of the res
for file in tqdm(res):
    segs = os.listdir(os.path.join(path,file,'segmentations'))
    for seg in segs:
        if seg.endswith('V1.nii.gz'):
            organ = seg[:-10]
            seg_path = os.path.join(path,file,'segmentations',organ+".nii.gz")
            mask = nib.load(seg_path).get_fdata()
            pseudo_label_path = os.path.join(path,file,'pseudo_label.nii.gz')
            pseudo_label_data = nib.load(pseudo_label_path).get_fdata()
            our_label = pseudo_label_data.copy()
            our_label[mask==1] = 0
