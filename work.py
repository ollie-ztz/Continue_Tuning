# TEMPLATE = {'spleen':1,'kidney_right':2,'kidney_left':3,'gall_bladder':4,'esophagus':5,'liver':6,'stomach':7,
#                     'aorta':8,'postcava':9,'portal_vein_and_splenic_vein':10,'pancreas':11,'adrenal_gland_right':12,'adrenal_gland_left':13,
#                     'duodenum':14,'hepatic_vessel':15,'lung_right':16,'lung_left':17,'colon':18,'intestine':19,'rectum':20,'bladder':21,'prostate':22,
#                     'femur_left':23,'femur_right':24,'celiac_truck':25,'kidney_tumor':26,'liver_tumor':27,'pancreas_tumor':28,'hepatic_vessel_tumor':29,
#                     'lung_tumor':30,'colon_tumor':31,'kidney_cyst':32}

# import numpy as np
# import nibabel as nib
# import os
# from tqdm import tqdm

# # Replace the label in pseudo_label.nii.gz if the organ in segmentations has revised version
# res =[]
# path = '/mnt/tzhang85/AbdomenAtlas_8K_internal'
# dataset_name = '08_AbdomenCT-1K'
# files_list = os.listdir(path)
# for file in tqdm(files_list):
#     if file.startswith(dataset_name):
#         segs = os.listdir(os.path.join(path,file,'segmentations'))
#         for seg in segs:
#             if seg.endswith('V1.nii.gz'):
#                 res.append(file)
# res = np.unique(res)
# # Replace the label in pseudo_label.nii.gz if the organ in segmentations has revised version with the help of the res
# for file in tqdm(res):
#     segs = os.listdir(os.path.join(path,file,'segmentations'))
#     for seg in segs:
#         if seg.endswith('V1.nii.gz'):
#             organ = seg[:-10]
#             seg_path = os.path.join(path,file,'segmentations',organ+".nii.gz")
#             mask = nib.load(seg_path).get_fdata()
#             pseudo_label_path = os.path.join(path,file,'pseudo_label.nii.gz')
#             pseudo_label_data = nib.load(pseudo_label_path).get_fdata()
#             affine = pseudo_label_data.affine
#             our_label = pseudo_label_data.copy()
#             cri = TEMPLATE[organ]
#             zero_mask = (pseudo_label_data==cri)
#             our_label[zero_mask==1] = 0
#             our_label[mask==1] = cri
#             our_label = nib.Nifti1Image(our_label, affine=affine)
#             filename = os.path.join(path,file,'pseudo_label.nii.gz')
#             nib.save(our_label, filename)

#08_AbdomenCT-1K_Case_00292_0000/ct.nii.gz	08_AbdomenCT-1K_Case_00292_0000/pseudo_label.nii.gz
import os
import numpy as np
from tqdm import tqdm

path = '/mnt/tiezheng/continue_learning_data/08_Swinonehot_R2'
epoch = '440'
dataset_name = '14_FELIX'
files_list = os.listdir(os.path.join(path,epoch,dataset_name))

txt_path = '/data2/tzhang/continue_learning/CLIP_Based_Continue_Learning/dataset/dataset_list/dice_14.txt'
txt = []
with open(txt_path,'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        line = line.split('\t')
        txt.append(line[0].split('/')[-1][:-7])
txt = np.unique(txt)
# 14_FELIX/img/FELIX5056_VENOUS.nii.gz	14_FELIX/label/FELIX5056_VENOUS.nii.gz
lines = []
for f in tqdm(txt):
    if f in files_list:
        continue
    else:
        line = os.path.join(dataset_name,'img',f+'.nii.gz')+'\t'+ os.path.join(dataset_name,'label'+f+'.nii.gz')
        lines.append(line)
with open('/data2/tzhang/continue_learning/CLIP_Based_Continue_Learning/dataset/dataset_list/Missing_440.txt','w') as file:
    for line in lines:
        file.write(line+'\n')
    file.close()