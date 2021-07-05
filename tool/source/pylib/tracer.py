import time
import sys
sys.path.append("..")
import os
from unidiff import PatchSet
# from ..run import get_children_process
import subprocess, psutil
btrace_home=os.path.abspath("./lib/btrace")

def get_children_process(pid):
    parent = psutil.Process(pid)
    children = parent.children(recursive=True)
    return children

def kill_proc_tree(children, including_parent=True):
    for child in children:
        child.kill(9)
    gone, still_alive = psutil.wait_procs(children, timeout=5)
    for child in still_alive:
        child.kill(9)

def extract_trace(src,tgt,start,end):
    s=''
    f=open(src)
    for line in f:
        if line.startswith('---'):
            cur=line.strip().split(':')[1]
            cur=int(cur)
            if cur>=start and cur<=end:
                s+=line
    f.close()
    f=open(tgt,'w')
    f.write(s)
    f.close()


def run(project,bugid,patch_no,tests, randoop_tests=[], task_list=[], tmp_tracefile='tmp_c', ):
    tmp_tracefile+=project+bugid+patch_no+'run_print_trace'
    tmp_tracefile=os.path.join(os.getcwd(),tmp_tracefile)
    w_buggy=project+str(bugid)+'b'
    w_patched=w_buggy+'_'+patch_no

    patchfile=os.path.join('../patches',patch_no)
    patch = PatchSet.from_filename(patchfile)

    source_file=patch[0].source_file
    target_file=patch[0].target_file
    line_no_list=[]
    for hunki in range(len(patch[0])):
        for i in range(len(patch[0][hunki])):
            if not patch[0][hunki][i].is_context:
                line_no_list.append(str(patch[0][hunki][i-1].source_line_no+1))
                break

    dir_path='../traces/'+w_patched
    if(os.path.exists(tmp_tracefile)):
        os.system('rm '+tmp_tracefile)
    os.system('mkdir '+dir_path)
    os.system('mkdir '+os.path.join(dir_path,'buggy'))
    os.system('mkdir '+os.path.join(dir_path,'patched'))
    os.system('mkdir '+os.path.join(dir_path,'buggy_e'))
    os.system('mkdir '+os.path.join(dir_path,'patched_e'))

    patch_info_file="fdsa.txt"
    os.system("rm -rf "+patch_info_file)
    os.system('make PatchInfo ARGS="'+os.path.join('../source/',source_file)+' '+patch_info_file+' '+','.join(line_no_list)+'" >/dev/null')
    f=open(patch_info_file)
    lines=f.readlines()
    patched_class=lines[-1].strip()
    patched_method,method_signature,start_line,end_line=lines[0].strip().split('\t')
    f.close()
    start_line=int(start_line)
    end_line=int(end_line)

    os.system('defects4j compile -w '+w_buggy)
    os.system('defects4j compile -w '+w_patched)


    f=open("%s/AllLines_pattern.java"%(btrace_home))
    s=f.read()
    f.close()
    s=s.replace('__CLASS__NAME__',patched_class)
    f=open("%s/AllLines.java"%(btrace_home),'w')
    f.write(s)
    f.close()
    os.system("cd %s && ./btracec AllLines.java"%(btrace_home))

    jvmargs=" -a -Djvmargs=\-javaagent:%s/btrace\-agent.jar=noserver,debug=true,scriptOutputFile=%s,script=%s/AllLines.class" % (btrace_home, tmp_tracefile, btrace_home)

    for test in tests:
        test=test.strip()
        
        # os.system('timeout 90 defects4j test -n -t '+test+' -w '+w_buggy+jvmargs)
        p = subprocess.Popen('timeout 90 defects4j test -n -t '+test+' -w '+w_buggy+jvmargs, shell=True)
        task_list.append(os.getpgid(p.pid))
        if os.path.exists(tmp_tracefile):
            extract_trace(tmp_tracefile,os.path.join(dir_path,'buggy_e','__'.join(test.split('::'))),start_line,end_line)
            os.system('mv '+tmp_tracefile+' '+os.path.join(dir_path,'buggy','__'.join(test.split('::'))))


        os.system('timeout 90 defects4j test -n -t '+test+' -w  '+w_patched+jvmargs)
        p = subprocess.Popen('timeout 90 defects4j test -n -t '+test+' -w  '+w_patched+jvmargs, shell=True)
        task_list.append(os.getpgid(p.pid))
        if os.path.exists(tmp_tracefile):
            extract_trace(tmp_tracefile,os.path.join(dir_path,'patched_e','__'.join(test.split('::'))),start_line,end_line)
            os.system('mv '+tmp_tracefile+' '+os.path.join(dir_path,'patched','__'.join(test.split('::'))))
        print(task_list)

    cmpl_flag=True
    testfile='../test_gen_randoop/'+project+'/randoop/'+bugid+'/'+project+'-'+bugid+'b-randoop.'+bugid+'.tar.bz2'
    for Test_Case in randoop_tests:
        test='Randoop.'+Test_Case.strip()
        if(cmpl_flag):
            # os.system('timeout 90 defects4j test -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_buggy+jvmargs)
            p = subprocess.Popen('timeout 90 defects4j test -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_buggy+jvmargs, shell=True)
            task_list.append(os.getpgid(p.pid))
        else:
            # os.system('timeout 90 defects4j test -n -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_buggy+jvmargs)
            p = subprocess.Popen('timeout 90 defects4j test -n -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_buggy+jvmargs, shell=True)
            task_list.append(os.getpgid(p.pid))
        if os.path.exists(tmp_tracefile):
            extract_trace(tmp_tracefile,os.path.join(dir_path,'buggy_e','__'.join(test.split('::'))),start_line,end_line)
            os.system('mv '+tmp_tracefile+' '+os.path.join(dir_path,'buggy','__'.join(test.split('::'))))
        if(cmpl_flag):
            # os.system('timeout 90 defects4j test -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_patched+jvmargs)
            p = subprocess.Popen('timeout 90 defects4j test -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_patched+jvmargs, shell=True)
            task_list.append(os.getpgid(p.pid))
        else:
            # os.system('timeout 90 defects4j test -n -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_patched+jvmargs)
            p = subprocess.Popen('timeout 90 defects4j test -n -s '+testfile+' -t '+Test_Case.strip()+' -w '+w_patched+jvmargs, shell=True)
            task_list.append(os.getpgid(p.pid))
        if os.path.exists(tmp_tracefile):
            extract_trace(tmp_tracefile,os.path.join(dir_path,'patched_e','__'.join(test.split('::'))),start_line,end_line)
            os.system('mv '+tmp_tracefile+' '+os.path.join(dir_path,'patched','__'.join(test.split('::'))))
        cmpl_flag=False
        print(task_list)

