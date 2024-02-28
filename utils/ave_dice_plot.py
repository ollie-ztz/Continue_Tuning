# generate a plot of the data from the csv file
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# load the data
organs = ['Liver', 'RKD', 'Spleen', 'Pancreas', 'Aorta', 'Postcava','Gall Bladder','Stomach','LKD']



def Cal_dice_thr_csv(csv_file, threshold):
    data = pd.read_csv(csv_file, header=None)
    # remove the column with the name of the organs on the first row
    # reomve_organs = ['adrenal_gland_right','adrenal_gland_left','duodenum','colon']
    removed_columns =[data.columns[7],data.columns[8],data.columns[11],data.columns[13]]
    data = data.drop(columns=removed_columns)
    data = data.iloc[1:,1:]

    # convert the data to numeric numbers if there are numbers in the data
    data = data.apply(pd.to_numeric, errors='coerce')
    # convert the value one or value smaller than thereshold to NAN
    data[data < threshold] = np.nan
    data[data == 1] = np.nan
    for i in range(len(data.columns)):
        data.columns.values[i] = i+1
    # calculate the mean value of each column of the data
    dice_scores = []
    for i in range(1, len(organs)+1):
        dice_scores.append(np.nanmean(data[i]))
    for i in range(len(dice_scores)):
        if np.isnan(dice_scores[i]):
            dice_scores[i] = 0
    # revised_organ_dice = (dice_scores[4]+dice_scores[5]+dice_scores[6]+dice_scores[7])/4
    # non_revised_organ_dice = (dice_scores[0]+dice_scores[1]+dice_scores[2]+dice_scores[3]+dice_scores[8])/5
    return dice_scores



# calculate the dice score of the data with threshold 1e-4
# dice_before_path = '/Users/ollie/Documents/General/CL/data_dice/dice_before.csv'
# dice_after_460_path = '/Users/ollie/Documents/General/CL/data_dice/dice_after_part_460.csv'
# dice_after_470_path = '/Users/ollie/Documents/General/CL/data_dice/dice_after_part_470.csv'
# dice_after_480_path = '/Users/ollie/Documents/General/CL/data_dice/dice_after_part_480.csv'
# dice_after_490_path = '/Users/ollie/Documents/General/CL/data_dice/dice_after_part_490.csv'
# dice_after_550_path = '/Users/ollie/Documents/General/CL/data_dice/dice_after_part_550.csv'

# dice_before = Cal_dice_thr_csv(dice_before_path, 1e-4)
# ave_re_before = (dice_before[4]+dice_before[5]+dice_before[6]+dice_before[7])/4
# ave_non_before = (dice_before[0]+dice_before[1]+dice_before[2]+dice_before[3]+dice_before[8])/5
# dice_after_460 = Cal_dice_thr_csv(dice_after_460_path, 1e-4)
# ave_re_460 = (dice_after_460[4]+dice_after_460[5]+dice_after_460[6]+dice_after_460[7])/4
# ave_non_460 = (dice_after_460[0]+dice_after_460[1]+dice_after_460[2]+dice_after_460[3]+dice_after_460[8])/5
# dice_after_470  = Cal_dice_thr_csv(dice_after_470_path, 1e-4)
# ave_re_470 = (dice_after_470[4]+dice_after_470[5]+dice_after_470[6]+dice_after_470[7])/4
# ave_non_470 = (dice_after_470[0]+dice_after_470[1]+dice_after_470[2]+dice_after_470[3]+dice_after_470[8])/5
# dice_after_480  = Cal_dice_thr_csv(dice_after_480_path, 1e-4)
# ave_re_480 = (dice_after_480[4]+dice_after_480[5]+dice_after_480[6]+dice_after_480[7])/4
# ave_non_480 = (dice_after_480[0]+dice_after_480[1]+dice_after_480[2]+dice_after_480[3]+dice_after_480[8])/5
# dice_after_490  = Cal_dice_thr_csv(dice_after_490_path, 1e-4)
# ave_re_490 = (dice_after_490[4]+dice_after_490[5]+dice_after_490[6]+dice_after_490[7])/4
# ave_non_490 = (dice_after_490[0]+dice_after_490[1]+dice_after_490[2]+dice_after_490[3]+dice_after_490[8])/5
# dice_after_550  = Cal_dice_thr_csv(dice_after_550_path, 1e-4)
# ave_re_550 = (dice_after_550[4]+dice_after_550[5]+dice_after_550[6]+dice_after_550[7])/4
# ave_non_550 = (dice_after_550[0]+dice_after_550[1]+dice_after_550[2]+dice_after_550[3]+dice_after_550[8])/5

dice_08_before = '/home/tzhang85/Continue_Tuning_ISBI2024/Dice_record/Unet_proof/dice_250.csv'
dice_08_after_260 = '/home/tzhang85/Continue_Tuning_ISBI2024/Dice_record/Unet_proof/dice_250.csv'
dice_08_after_270 = '/home/tzhang85/Continue_Tuning_ISBI2024/Dice_record/Unet_proof/dice_250.csv'
dice_08_after_280 = '/home/tzhang85/Continue_Tuning_ISBI2024/Dice_record/Unet_proof/dice_250.csv'
dice_08_after_290 = '/home/tzhang85/Continue_Tuning_ISBI2024/Dice_record/Unet_proof/dice_250.csv'
dice_08_after_350 = '/home/tzhang85/Continue_Tuning_ISBI2024/Dice_record/Unet_proof/dice_250.csv'
dice_before = Cal_dice_thr_csv(dice_08_before, 1e-4)
dice_after_260 = Cal_dice_thr_csv(dice_08_after_260, 1e-4)
dice_after_270 = Cal_dice_thr_csv(dice_08_after_270, 1e-4)
dice_after_280 = Cal_dice_thr_csv(dice_08_after_280, 1e-4)
dice_after_290 = Cal_dice_thr_csv(dice_08_after_290, 1e-4)
dice_after_350 = Cal_dice_thr_csv(dice_08_after_350, 1e-4)

print(dice_before)
print(dice_after_260)
print(dice_after_270)
print(dice_after_280)
print(dice_after_290)
print(dice_after_350)

ave_re_before = (dice_before[4]+dice_before[5]+dice_before[6]+dice_before[7])/4
ave_non_before = (dice_before[0]+dice_before[1]+dice_before[2]+dice_before[3]+dice_before[8])/5

ave_260_re = (dice_after_260[4]+dice_after_260[5]+dice_after_260[6]+dice_after_260[7])/4
ave_260_non = (dice_after_260[0]+dice_after_260[1]+dice_after_260[2]+dice_after_260[3]+dice_after_260[8])/5

ave_270_re = (dice_after_270[4]+dice_after_270[5]+dice_after_270[6]+dice_after_270[7])/4
ave_270_non = (dice_after_270[0]+dice_after_270[1]+dice_after_270[2]+dice_after_270[3]+dice_after_270[8])/5

ave_280_re = (dice_after_280[4]+dice_after_280[5]+dice_after_280[6]+dice_after_280[7])/4
ave_280_non = (dice_after_280[0]+dice_after_280[1]+dice_after_280[2]+dice_after_280[3]+dice_after_280[8])/5

ave_290_re = (dice_after_290[4]+dice_after_290[5]+dice_after_290[6]+dice_after_290[7])/4
ave_290_non = (dice_after_290[0]+dice_after_290[1]+dice_after_290[2]+dice_after_290[3]+dice_after_290[8])/5

ave_350_re = (dice_after_350[4]+dice_after_350[5]+dice_after_350[6]+dice_after_350[7])/4
ave_350_non = (dice_after_350[0]+dice_after_350[1]+dice_after_350[2]+dice_after_350[3]+dice_after_350[8])/5


re_dice = [ave_re_before, ave_260_re, ave_270_re, ave_280_re, ave_290_re, ave_350_re]
non_dice = [ave_non_before, ave_260_non, ave_270_non, ave_280_non, ave_290_non, ave_350_non]
aorta = [dice_before[4], dice_after_260[4], dice_after_270[4], dice_after_280[4], dice_after_290[4] ,dice_after_350[4]]

# re_dice = [ave_re_before, ave_re_460, ave_re_470, ave_re_480, ave_re_490, ave_re_550]
# non_dice = [ave_non_before, ave_non_460, ave_non_470, ave_non_480, ave_non_490, ave_non_550]
# Aorta = [dice_before[4], dice_after_460[4], dice_after_470[4], dice_after_480[4], dice_after_490[4] ,dice_after_550[4]]
# # plot the two dice scores on the same plot and compare them
# # add the points on the line

x = np.arange(6)
plt.plot(x, re_dice, marker='.', label='Revised_organs')
plt.plot(x, non_dice, marker='*', label='Non-revised organs')
plt.plot(x, aorta, marker='o', label='Aorta')
plt.xticks(x, ['Base', '10', '20', '30' ,'40','100'])
plt.xlabel('epoches')
plt.ylabel('Dice score')
plt.legend()
plt.show()