import os
import re
from time import ctime
import subprocess

try:
    from git import *
except:
    print("run pip install GitPython")
    exit()

GIT_CLONE_CMD = 'git clone {} {}'
_repo_name_re = re.compile(br'/([a-zA-Z0-9 ]+).git')

DEFAULT_CONFIG_FILE = os.path.expanduser('~/.grm_config')
DEFAULT_REPO_DIR = os.path.expanduser('~/.grm')

DEFAULT_REPO_LOG = '{}/.log'.format(DEFAULT_REPO_DIR)

DEFAULT_REPO_LIST = '{}/.list'.format(DEFAULT_REPO_DIR)

if not os.access(DEFAULT_CONFIG_FILE, os.F_OK):
    os.mknod(DEFAULT_CONFIG_FILE)
if not os.access(DEFAULT_REPO_DIR, os.F_OK):
    os.mkdir(DEFAULT_REPO_DIR)
if not os.access(DEFAULT_REPO_LOG, os.F_OK):
    os.mknod(DEFAULT_REPO_LOG)
if not os.access(DEFAULT_REPO_LIST, os.F_OK):
    os.mknod(DEFAULT_REPO_LIST)

def execve(cmd):
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    retcode = p.wait()
    out = p.stdout.read()
    err = p.stderr.read()
    
    f = open(DEFAULT_REPO_LOG, 'a')
    f.write('[{}]\nexec:{}\nretcode:{}\nout:\n{}\nerr:\n{}\n'.format(ctime(), cmd, retcode, out, err))
    f.close()
    
    return retcode, out, err
    
def repo_chk(list):
    ret = []
    for repo_name in list:
        if os.access('{}/{}'.format(DEFAULT_REPO_DIR, repo_name), os.F_OK):
            ret.append(repo_name)
        else:
            f = open(DEFAULT_REPO_LOG, 'a')
            f.write('[{}]\n{} no longger exists\n'.format(ctime(), repo_name))
            f.close()
    return ret
    
def repo_list():
    list = open(DEFAULT_REPO_LIST).read().split()
    new_list = repo_chk(list)
    f = open(DEFAULT_REPO_LIST, 'w')
    f.writelines(new_list)
    f.close()
    return new_list
    
def list_repo():
    banner = 'Git Repository List'
    print(banner)
    for repo_name in repo_list():
        print(repo_name)
        
def remove_repo(repo_name):
    
    if repo_name in repo_list():
        dir = '{}/{}'.format(DEFAULT_REPO_DIR, repo_name)
        retcode, out, err = execve('rm -rf {}'.format(dir))
        
    else:
        print('no such repo')
    
def clone_repo(url):
    
    repo_name = _repo_name_re.findall(url)[0]
    cmd = GIT_CLONE_CMD.format(url, '{}/{}'.format(DEFAULT_REPO_DIR, repo_name))
    retcode, out, err = execve(cmd)
    
    if retcode == 0:
        f = open(DEFAULT_REPO_LIST, 'w+')
        f.write('{}\n'.format(repo_name))
        f.close()
        
        
if __name__ == '__main__':
    clone_repo('https://github.com/matrix1001/psguard.git')
    list_repo()
    remove_repo('psguard')
    list_repo()
    
    