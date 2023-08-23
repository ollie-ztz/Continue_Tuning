import numpy as np
import nibabel as nib
import os
from tqdm import tqdm
import argparse
import shutil
import cc3d

TEMPLATE = {'spleen':1,'kidney_right':2,'kidney_left':3,'gall_bladder':4,'esophagus':5,'liver':6,'stomach':7,
                    'aorta':8,'postcava':9,'portal_vein_and_splenic_vein':10,'pancreas':11,'adrenal_gland_right':12,'adrenal_gland_left':13,
                    'duodenum':14,'hepatic_vessel':15,'lung_right':16,'lung_left':17,'colon':18,'intestine':19,'rectum':20,'bladder':21,'prostate':22,
                    'femur_left':23,'femur_right':24,'celiac_truck':25,'kidney_tumor':26,'liver_tumor':27,'pancreas_tumor':28,'hepatic_vessel_tumor':29,
                    'lung_tumor':30,'colon_tumor':31,'kidney_cyst':32}



def generate_part_label(args,case_path,save_path,revised_file_list):
    pseudo_label_file = os.path.join(case_path,'pseudo_label.nii.gz')
    pseudo_label = nib.load(pseudo_label_file)
    pseudo_label_data = pseudo_label.get_fdata()
    affine = pseudo_label.affine
    our_label = pseudo_label_data.copy()
    # mask = np.zeros_like(pseudo_label_data)
    for i in range(len(revised_file_list)):
        organ = revised_file_list[i][:-10]
        cri = TEMPLATE[organ]
        if i == 0:
            mask = (pseudo_label_data==cri)
        else:
            mask = (mask) | (pseudo_label_data==cri)
    our_label[mask!=1] = 0
    our_label = nib.Nifti1Image(our_label, affine=affine)
    filename = os.path.join(save_path,'pseudo_part_label.nii.gz')
    nib.save(our_label, filename)
    shutil.copy(os.path.join(case_path,'ct.nii.gz'),os.path.join(save_path,'ct.nii.gz'))



def main_process(args,cases_list):
    for i in tqdm(range(len(cases_list))):
        case = cases_list[i]
        case_path = os.path.join(args.data_path,case)
        seg_path = os.path.join(case_path,'segmentations')
        revised_version = args.version
        revised_file_list = os.listdir(seg_path)
        revised_file_list = [f for f in revised_file_list if f.endswith(revised_version+'.nii.gz') and not f.startswith('.')]
        if len(revised_file_list)==0:
            print('No revised file in this case')
            continue
        else:
            save_path = os.path.join(args.save_dir,args.dataset,case)
            if not os.path.exists(save_path):
                os.mkdir(save_path)
            else:
                print('The saving directory exists')
            generate_part_label(args,case_path,save_path,revised_file_list)



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', default='/mnt/tzhang85/AbdomenAtlas_8K_internal', help='The path of your data')
    parser.add_argument('--save_dir', default='/mnt/tiezheng/continue_learning_data/asssemeble_data', help='The saving path')
    parser.add_argument('--dataset', default='08_AbdomenCT-1K', help='The dataset name')
    parser.add_argument('--version', default='V1', help='The version of revised label')

    args = parser.parse_args()

    save_dir = os.path.join(args.save_dir,args.dataset)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)
    else:
        print('The saving directory exists')


    cases_list = os.listdir(os.path.join(args.data_path))
    cases_list = sorted([f for f in cases_list if f.startswith(args.dataset)])
    main_process(args,cases_list)



if __name__ == "__main__":
    main()