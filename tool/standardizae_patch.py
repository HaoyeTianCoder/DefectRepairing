import os, fnmatch
import re

abpatch = ['AVATAR', 'DynaMoth', 'FixMiner', 'kPAR', 'TBar', 'Developer']
abLikePatch = ['Cardumen', 'jKali', 'jMutRepair',]
Kui_patch_path = '/Users/haoye.tian/Documents/University/data/APR-Efficiency-NFL'
patchsim_patch_path = '/Users/haoye.tian/Library/Containers/com.tencent.xinWeChat/Data/Library' \
                      '/Application Support/com.tencent.xinWeChat/2.0b4.0.9/ee436899d181321caa2a2b54b9947702/Message/MessageTemp/8ab4e803e2aec02f03b28690d2dcd401/File/patches'

def parse_abpatch(path, tool):
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                print (file)
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f:
                    for line in f:
                        if line.startswith('diff ') or line.startswith('index '):
                            continue
                        elif line.startswith('--- ') or line.startswith('+++ '):
                            origin_head = line.split(' ')[1].split('\t')[0].strip()
                            new_head = line.split(' ')[0] + ' ' + origin_head[1:] + '\n'
                            new_line += new_head
                        else:
                            new_line += line
                with open(os.path.join(root, file), 'w+') as f:
                    f.write(new_line)
def find_source_path(path, tool):
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                print (file)
                project = file.split('-')[1]
                id = file.split('-')[2].split('_')[0]
                label = root.split('/')[-6]
                if label == 'Correct':
                    folder_target = project+'-'+id+'_C'
                elif label == 'Incorrect':
                    folder_target = project+'-'+id+'_P'
                path_target = os.path.join(Kui_patch_path, tool, folder_target)
                patch_target = os.listdir(path_target)
                bug_localization = ''
                with open(path_target + '/' + patch_target[0], 'r+') as f1:
                    for line in f1:
                        if line.startswith('PATCH_DIFF_ORIG'):
                            bug_localization_list = line.split(' ')[1].split('/')[3:]
                            bug_localization = '/' + '/'.join(bug_localization_list)
                            bug_localization = bug_localization[:-5] + '.java'

                new_line = ''
                with open(os.path.join(root, file), 'r+') as f2:
                    for line in f2:
                        if line.startswith('--- '):
                            new_line += '--- ' + bug_localization + '\n'
                        elif line.startswith('+++ '):
                            new_line += '+++ ' + bug_localization + '\n'
                        else:
                            new_line += line
                with open(os.path.join(root, file), 'w+') as f3:
                    f3.write(new_line)

def find_patchsim_path(path, tool):
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                print (file)
                project = file.split('-')[1]
                id = file.split('-')[2].split('_')[0]
                label = root.split('/')[-6]
                folder_target_head = 'Pat-' + label + '-' + project+'-'+id
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f1:
                    for line in f1:
                        if line.startswith('--- '):
                            source_file = line.split(' ')[1].split('/')[10] + '.java'
                            source_path = search_source_path(patchsim_patch_path, folder_target_head, source_file)
                            new_line += '--- ' + source_path + '\n'
                        elif line.startswith('+++ '):
                            source_file = line.split(' ')[1].split('/')[10] + '.java'
                            source_path = search_source_path(patchsim_patch_path, folder_target_head, source_file)
                            new_line += '+++ ' + source_path + '\n'
                        else:
                            new_line += line

                with open(os.path.join(root, file), 'w+') as f2:
                    f2.write(new_line)



def search_source_path(patchsim_patch_path, folder_target_head, source_file):
    for root2, dirs2, files2 in os.walk(patchsim_patch_path):
        for file2 in files2:
            if file2.startswith(folder_target_head):
                with open(os.path.join(root2, file2), 'r+') as f2:
                    for line in f2:
                        if line.startswith('--- '):
                            line = re.split(' |\t', line)[1]
                            if line.endswith(source_file):
                                result_list = line.split('/')[1:]
                                result = '/' + '/'.join(result_list)
                                return result

def parse_3s_Gen_ConFix_KaliA(path, tool):
    # parse_3s_Gen_ConFix_KaliA
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                project = file.split('-')[1]
                id = file.split('-')[2].split('_')[0]
                print (file)
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f:
                    for line in f:
                        if line.startswith('diff ') or line.startswith('index '):
                            continue
                        elif line.startswith('--- '):
                            origin_head = line.split(' ')[1].split('\t')[0].strip()
                            if tool == '3sFix':
                                new_head_list = origin_head.split('/')[5:]
                                new_head_minus = '--- /' + '/'.join(new_head_list) + '\n'

                                if project == 'Math' and int(id) >= 85:
                                    new_head_minus = new_head_minus.replace('/src/default/', '/src/java/')
                                elif project == 'Lang' and int(id) >= 36:
                                    new_head_minus = new_head_minus.replace('/src/default/', '/src/java/')
                                elif project == 'Chart':
                                    new_head_minus = new_head_minus.replace('/src/default/', '/source/')
                                elif project == 'Closure':
                                    new_head_minus = new_head_minus.replace('/src/default/', '/src/')
                                elif project == 'Lang' or project == 'Math' or project == 'Time':
                                    new_head_minus = new_head_minus.replace('/src/default/', '/src/main/java/')
                                elif project == 'Mockito':
                                    new_head_minus = new_head_minus.replace('/src/default/', '/src/')
                            elif tool == 'ConFix':
                                new_head_list = origin_head.split('/')[5:]
                                new_head_minus = '/'.join(new_head_list) + '\n'

                                if project == 'Math' and int(id) >= 85:
                                    new_head_minus = '/src/java/' + new_head_minus
                                elif project == 'Lang' and int(id) >= 36:
                                    new_head_minus = '/src/java/' + new_head_minus
                                elif project == 'Chart':
                                    new_head_minus = '/source/' + new_head_minus
                                elif project == 'Closure':
                                    new_head_minus = '/src/' + new_head_minus
                                elif project == 'Lang' or project == 'Math' or project == 'Time':
                                    new_head_minus = '/src/main/java/' + new_head_minus
                                elif project == 'Mockito':
                                    new_head_minus = '/src/' + new_head_minus
                                new_head_minus = '--- ' + new_head_minus
                            elif tool == 'GenProgA' or 'KaliA':
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

def parse_kPAR(path, tool):
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                project = file.split('-')[1]
                id = file.split('-')[2].split('_')[0]
                print (file)
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f:
                    for line in f:
                        if line.startswith('diff ') or line.startswith('Index') or line.startswith('==='):
                            continue
                        # swap/fix the position of -- and ++
                        elif line.startswith('++'):
                            origin_head = line.split(' ')[1].split('\t')[0].strip()
                            if project == 'Math' and int(id) >= 85:
                                new_head_plus = '/src/java/' + origin_head
                            elif project == 'Lang' and int(id) >= 36:
                                new_head_plus = '/src/java/' + origin_head
                            elif project == 'Chart':
                                new_head_plus = '/source/' + origin_head
                            elif project == 'Closure':
                                new_head_plus = '/src/' + origin_head
                            elif project == 'Lang' or project == 'Math' or project == 'Time':
                                new_head_plus = '/src/main/java/' + origin_head
                            elif project == 'Mockito':
                                new_head_plus = '/src/' + origin_head
                            new_head_plus = '+++ ' + new_head_plus + '\n'
                        elif line.startswith('--'):
                            origin_head = line.split(' ')[1].split('\t')[0].strip()
                            if project == 'Math' and int(id) >= 85:
                                new_head_minus = '/src/java/' + origin_head
                            elif project == 'Lang' and int(id) >= 36:
                                new_head_minus = '/src/java/' + origin_head
                            elif project == 'Chart':
                                new_head_minus = '/source/' + origin_head
                            elif project == 'Closure':
                                new_head_minus = '/src/' + origin_head
                            elif project == 'Lang' or project == 'Math' or project == 'Time':
                                new_head_minus = '/src/main/java/' + origin_head
                            elif project == 'Mockito':
                                new_head_minus = '/src/' + origin_head
                            new_head_minus = '--- ' + new_head_minus + '\n'
                            # new_line += new_head_minus + new_head_plus
                        else:
                            new_line += line
                new_line = new_head_minus + new_head_plus + new_line
                with open(os.path.join(root, file), 'w+') as f:
                    f.write(new_line)

if __name__ == '__main__':
    # fix head indicator(path ---, +++) of patch.
    path = '/Users/haoye.tian/Documents/tmp'
    tools = os.listdir(path)
    for tool in tools:
        if tool in abpatch:
            parse_abpatch(path, tool)
        elif tool in abLikePatch:
            find_source_path(path, tool)
        elif tool == '3sFix' or tool == 'GenProgA' or tool == 'ConFix' or tool == 'KaliA':
            parse_3s_Gen_ConFix_KaliA(path, tool)
        elif tool == 'PraPR':
            parse_kPAR(path, tool)
        elif tool == 'PatchSim':
            find_patchsim_path(path, tool)
