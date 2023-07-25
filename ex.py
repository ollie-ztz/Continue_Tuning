# read the PAOT_08.txt file 


import os

path = '/mnt/tzhang85/AbdomenAtlas_8K_internal'
files = os.listdir(path)
files = sorted([f for f in files if f.startswith('08_AbdomenCT-1K')])
lines = []
for f in files:
    line = os.path.join(f, 'ct.nii.gz') + '\t' + os.path.join(f,'pseudo_label.nii.gz')
    lines.append(line)
out = './dataset/dataset_list'
save_file = 'PAOT_08_CL.txt'
with open(os.path.join(out, save_file), 'w') as f:
    f.write('\n'.join(lines))
    