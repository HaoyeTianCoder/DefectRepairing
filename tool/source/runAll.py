#!/usr/bin/python
import sys, os, subprocess,fnmatch,csv,re
import time
from run import run
# sys.path.append('')

if __name__ == '__main__':
    exist_result = set()
    if os.path.exists('RESULT.csv'):
       csv_reader = csv.reader(open('RESULT.csv'))
       for line in csv_reader:
           patch_name = line[0]
           exist_result.add(patch_name)

    listdirs = os.listdir('../patches')
    currentpath=os.path.dirname(os.path.realpath(__file__))
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    for f in listdirs:
        pattern = 'patch*rrect'
        if fnmatch.fnmatch(f, pattern):
           print(f)
           if f in exist_result:
               print("{}'s result exists".format(f))
               continue
           with open(currentpath+'/../patches/'+f) as file:
               arraynames=f.split("-")
               project= arraynames[1]
               bug= arraynames[2].split("_")[0]

               # os.chdir('')
               # os.system('python3 run.py '+project+'  '+bug+'  '+f)
               run(project, bug, f)
               # os.chdir('../..')


