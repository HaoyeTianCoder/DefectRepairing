#!/usr/bin/python
import sys, os, subprocess,fnmatch,csv,re
import multiprocessing
import csv

cores = multiprocessing.cpu_count()
print "cores: ", cores
pool = multiprocessing.Pool(processes=cores)

def run_cmd(cmd):
    os.system(cmd)

if __name__ == '__main__':
   # with open('./source/RESULT.csv', ) as f:
   exist_result = set()
   csv_reader = csv.reader(open('./source/RESULT.csv'))
   for line in csv_reader:
       patch_name = line[0]
       exist_result.add(patch_name)

   listdirs = os.listdir('./patches')
   currentpath=os.path.dirname(os.path.realpath(__file__))
   r = re.compile("([a-zA-Z]+)([0-9]+)")
   cmd_list = []
   for f in listdirs:
        pattern = 'patch*rrect'
        if fnmatch.fnmatch(f, pattern):
           print(f)
           if f in exist_result:
               print("{}'s result exists".format(f))
               continue
           with open(currentpath+'/patches/'+f) as file:
               arraynames=f.split("-")  
               project= arraynames[1]
               bug= arraynames[2].split("_")[0]
               cmd = 'python3 run.py '+project+'  '+bug+'  '+f
               cmd_list.append(cmd)

   os.chdir('source')
   pool.map(run_cmd, cmd_list)
   os.chdir('..')
