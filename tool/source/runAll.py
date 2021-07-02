#!/usr/bin/python
import sys, os, subprocess,fnmatch,csv,re
import time
from run import run
import multiprocessing
# sys.path.append('')
import signal

cores = multiprocessing.cpu_count()
print ("cores: ", cores)
pool = multiprocessing.Pool(processes=cores)


def handler(signum, frame):
   # print("time out!")
   raise Exception("TimeOut")

def runMain(para_list):
    project, bug, f = para_list[0], para_list[1], para_list[2]
    info = ''

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(3600)
    start = time.time()
    try:
        run(project, bug, f)
    except Exception as e:
        info = e
        print(e)
    end = time.time()
    signal.alarm(0)

    if info != '':
        during = info
    else:
        during = str(end - start)
    with open('./time.csv', 'a') as timefile:
        filewriter = csv.writer(timefile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow([f, during])


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
    cmd_list = []
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
               cmd_list.append([project, bug, f])
               # os.chdir('../..')

    pool.map(runMain, cmd_list)


