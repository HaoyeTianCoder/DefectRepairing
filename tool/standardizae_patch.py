import os, fnmatch

abpatch = ['AVATAR', 'DynaMoth', 'FixMiner', 'kPAR', 'TBar', 'Developer']

def parse_abpatch(path, tool):
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                print file
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

def parse_3sGen(path, tool):
    new_path = os.path.join(path, tool)
    pattern = '*.patch'
    for root, dirs, files in os.walk(new_path):
        for file in files:
            if fnmatch.fnmatch(file, pattern):
                print file
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f:
                    for line in f:
                        if line.startswith('diff ') or line.startswith('index '):
                            continue
                        elif line.startswith('--- '):
                            origin_head = line.split(' ')[1].split('\t')[0].strip()
                            if tool == '3sFix':
                                new_head_list = origin_head.split('/')[5:]
                            elif tool == 'GenProgA':
                                new_head_list = origin_head.split('/')[3:]
                            new_head_minus = '--- /' + '/'.join(new_head_list) + '\n'
                            new_line += new_head_minus
                        elif line.startswith('+++ '):
                            new_head_plus = '+++ /' + '/'.join(new_head_list) + '\n'
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
                print file
                new_line = ''
                with open(os.path.join(root, file), 'r+') as f:
                    for line in f:
                        if line.startswith('diff ') or line.startswith('Index') or line.startswith('==='):
                            continue
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
    path = '/Users/haoye.tian/Documents/available'
    tools = os.listdir(path)
    for tool in tools:
        if tool in abpatch:
            parse_abpatch(path, tool)
        elif tool == '3sFix' or tool == 'GenProgA':
            parse_3sGen(path, tool)

        elif tool == 'PraPR':
            parse_kPAR(path, tool)
