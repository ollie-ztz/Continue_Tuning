# read the PAOT_08.txt file 


import os

path = '/mnt/tzhang85/AbdomenAtlas_8K_internal'
files = sorted(os.listdir(path))[:200]
# files = sorted([f for f in files if f.startswith('08_AbdomenCT-1K')])
lines = []
for f in files:
    line = os.path.join(f, 'ct.nii.gz') + '\t' + os.path.join(f,'segmentations')
    lines.append(line)
out = './dataset/dataset_list'
save_file = 'chongyusb.txt'
with open(os.path.join(out, save_file), 'w') as f:
    f.write('\n'.join(lines))
    