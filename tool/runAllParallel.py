#!/usr/bin/python
import sys, os, subprocess,fnmatch,csv,re
import multiprocessing

cores = multiprocessing.cpu_count()
print "cores: ", cores
pool = multiprocessing.Pool(processes=cores)

def run_cmd(cmd):
    os.system(cmd)

if __name__ == '__main__':
   listdirs = os.listdir('./patches')
   currentpath=os.path.dirname(os.path.realpath(__file__))
   r = re.compile("([a-zA-Z]+)([0-9]+)")
   cmd_list = []
   for f in listdirs:
        pattern = 'patch*rrect'
        if fnmatch.fnmatch(f, pattern):
           print(f) 
           with open(currentpath+'/patches/'+f) as file:
               arraynames=f.split("-")  
               project= arraynames[1]
               bug= arraynames[2].split("_")[0]
               cmd = 'python3 run.py '+project+'  '+bug+'  '+f
               cmd_list.append(cmd)

   os.chdir('source')
   pool.map(run_cmd, cmd_list)
   os.chdir('..')
