import gevent.subprocess as sp
import gevent
from gevent.pool import Pool
import sys

from os.path import dirname
import collections

class logger(object):
    def __init__(self, file=None):
        self.terminal = sys.stdout
        self.log = None 
        if file :
            ensure_dir(dirname(file))
            self.log = open(file, "a")

    def write(self,msg):
        self.terminal.write(msg)
        if self.log:
            self.log.write(msg)

    def flush(self):
        self.terminal.flush()
        if self.log:
            self.log.flush()

    def __del__(self):
        if self.log :
            self.log.close()
            
    
def pipebash(cmd, cwd=None, input=None ):
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, 
                 stderr=sp.PIPE, stdin=sp.PIPE, cwd=cwd )
    return p.communicate(input)



def runbash(cmd, file=None, cwd=None ):
    p = sp.Popen(cmd, shell=True, stdout=sp.PIPE, 
                 stderr=sp.PIPE, cwd=cwd )
    
    log = logger(file)
    while p.poll() is None:
            line = p.stdout.readline()
            if line:
                log.write(line)
                log.flush()

    if p.returncode > 0 :
        for line in iter(p.stderr.readline, b''):
            log.write(line)
            log.flush()

    return p.returncode


class bash(object):
    def __init__(self, file=None, cwd=None):
        ""
        self.cwd = cwd
        self.file = file

    def run(self, cmd, file=None):
        if not file:
            file=self.file
        code = runbash(cmd,file=file,cwd=self.cwd)
        return (code,file)

# using the gevent lib implemented coroutine async
def gmap(f, l, job=None):
    if job:
        p = Pool(job)
        R = p.map(f,l)
        p.join()
    else:
        G = [ gevent.spawn(f, i) for i in l ]
        gevent.joinall(G)
        R = [ g.value for g in G]

    return  R

def deep_run(func, l):
    if not l:
        return
    if isinstance(l, collections.Iterable) and not isinstance(l, str):
        map(lambda x: deep_run(func,x), l)
    else:
        func(l)

