#!/usr/bin/python
import sys, os, subprocess,fnmatch, shutil, csv,re, datetime

#This script transfers all patches from Defects4j reloaded to the some format of test sim patches


def travFolder(dir):
   listdirs = os.listdir(dir)
   for f in listdirs:
       pattern = 'patch*.patch'
       if os.path.isfile(os.path.join(dir, f)):
           if fnmatch.fnmatch(f, pattern):
               label = dir.split('/')[5]
               benchmark = dir.split('/')[2]
               tool = dir.split('/')[4]
               arraynames=os.path.splitext(f)[0].split("-")
               #arraynames ['patch1', 'Chart', '1', 'CapGen']
               patchNo=arraynames[0]
               projectId=arraynames[1]
               projectId=projectId[0].upper() + projectId[1:]
               bugId=arraynames[2].split('_')[0]
               patchName='-'.join([patchNo, projectId, bugId]) + '_' + tool + '_' +benchmark + '_' + label
               print(patchName)

               # print (projectId)
               # print (bugId)
               patchcode=''
               try:
                   with open(dir+'/'+f, 'r') as rfile:
                       lines = rfile.read().split('\n')
                    #    print lines
                       for line in lines:
                           if "---" in line:
                               oldfirstline=line.split("---")[1].strip()
                               firstline=projectId+bugId+'b'+oldfirstline
                               print (firstline)
                           elif "+++" in line:
                               oldsecondline=line.split("+++")[1].strip()
                               secondline=projectId+bugId+'b_'+patchName+oldsecondline
                               print (secondline)
                           else:
                               patchcode+=line+'\n'
                               # print (patchcode)
                   # if not os.path.exists('./patches/'+dir[2:]):
                   #     os.makedirs('./patches/'+dir[2:])
                   with open('./patches/'+patchName,'a') as wfile:
                       wfile.write("diff -w -r -u "+firstline+" "+secondline+'\n')
                       wfile.write("--- "+firstline+'\n')
                       wfile.write("+++ "+secondline+'\n')
                       wfile.write(patchcode)
               except Exception as e:
                   print('parse error: {}'.format(e))
                                  
       else:
           if 'tmp.patch' not in f:
                travFolder(dir+'/'+f)



if __name__ == '__main__':
    os.system('mkdir ./patches')
    # folderdir='./3sFix'
    # folderdir='./PatchStanTOSEM' + sys.argv[1]
    folderdir='./PatchStand2_Merged'
    travFolder(folderdir)
