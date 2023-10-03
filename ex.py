import numpy as np
import nibabel as nib
import os
    
path = '/mnt/zzhou82/PublicAbdominalData/12_CT-ORG/label/labels-0.nii.gz'
img = nib.load(path)
data = img.get_fdata()
print(np.where(data==4))