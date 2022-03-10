import os, fnmatch
import re

def parse_patchNaturalnessYe(path):
    pattern = '*.patch'
    for root, dirs, files in os.walk(path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                project = file.split('-')[1]
                project = project[0].upper() + project[1:]
                id = file.split('-')[2].split('_')[0]
                print (file)
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f:
                    for line in f:
                        if line.startswith('diff ') or line.startswith('index '):
                            continue
                        elif line.startswith('--- '):
                            origin_head = line.split(' ')[1].split('\t')[0].strip()
                            new_head_list = origin_head.split('/')[3:]
                            new_head_minus = '--- /' + '/'.join(new_head_list) + '\n'
                            new_line += new_head_minus
                        elif line.startswith('+++ '):
                            new_head_plus = new_head_minus.replace('--- ', '+++ ')
                            new_line += new_head_plus
                        else:
                            new_line += line
                with open(os.path.join(root, file), 'w+') as f:
                    f.write(new_line)



if __name__ == '__main__':
    # fix head indicator(path ---, +++) of patch.
    path = '/Users/haoye.tian/Documents/PatchStand2_Merged'
    parse_patchNaturalnessYe(path)