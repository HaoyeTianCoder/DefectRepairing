import json
import os
import csv
import pandas as pd

PATCHSIM_RESULT_dict = {}
with open('RESULT_1.csv', 'r+') as f:
    for line in f:
        patchid = line.split(',')[0]
        head = patchid.split('_')[0]
        tool = patchid.split('_')[1]

        patch = head.split('-')[0]
        if '#' in patch:
            patch = patch.split('#')[0]
        project = head.split('-')[1]
        id = head.split('-')[2]
        new_head = '-'.join([patch, project, id])

        new_patch_id = new_head + '_' + tool + '_PatchNaturalness'
        new_patch_id = new_patch_id.lower()
        label = line.split(',')[3]
        if label == 'Correct':
            PATCHSIM_RESULT_dict[new_patch_id] = 1
        elif label == 'Incorrect':
            PATCHSIM_RESULT_dict[new_patch_id] = 0

with open('RESULT_09.csv', 'r+') as f:
    for line in f:
        patchid = line.split(',')[0]
        patchid = patchid.replace('_Correct', '').replace('_Incorrect', '')
        patchid = patchid.lower()
        label = line.split(',')[3]
        if label == 'Correct':
            PATCHSIM_RESULT_dict[patchid] = 1
        elif label == 'Incorrect':
            PATCHSIM_RESULT_dict[patchid] = 0

with open('RESULT_WASP.csv', 'r+') as f:
    for line in f:
        patchid = line.split(',')[0]
        patchid = patchid.replace('_Correct', '').replace('_Incorrect', '')
        patchid = patchid.lower()
        label = line.split(',')[3]
        if label == 'Correct':
            PATCHSIM_RESULT_dict[patchid] = 1
        elif label == 'Incorrect':
            PATCHSIM_RESULT_dict[patchid] = 0

with open('PATCHSIM_RESULT.json', 'w+') as f:
    json.dump(PATCHSIM_RESULT_dict, f)





