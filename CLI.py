# PYTHON scripting lib
# imports all the necessary tools to make it a replacement for bash
# 

import os,sys
from sys import stderr
from sys import stdout
from sys import stdin

class file:
    def __init__(self,filename):
        self.path = os.path.abspath(os.path.expanduser(filename))
        self.name = os.path.split(self.path)[1]
        self.ext = os.path.splitext(self.path)[1]
        self.exists = os.path.exists(self.path)

def parse_args(argv,fmt):
    """
    fmt is a list of tuples as (shortopt,longopt,arguments,...)
    returns a tuple with a the first entry the remaining arguments
    and the second a list of lists of arguments for each opt prepended by the longopt
    """
    args = []
    opts = []
    i = 0

    while i < len(argv):
        if argv[i][:2] == "--":
            suc = 0
            for f in fmt:
                if f[1] == argv[i][2:] and len(argv) - i > f[2]:
                    opts.append([f[1]] + argv[i+1:i+1+f[2]])
                    i+=f[2]
                    suc = 1
                    break
            if suc == 0:
                print >>stderr,"Option",argv[i],"failed"
                raise IOError
        elif argv[i][0] == "-":
            suc = 0
            for f in fmt:
                if f[0] == argv[i][1:] and len(argv) - i > f[2]:
                    opts.append([f[1]]+argv[i+1:i+1+f[2]])
                    i+=f[2]
                    suc = 1
                    break
            if suc == 0:
                print >>stderr,"Option",argv[i],"failed"
                raise IOError
        else:
            args.append(argv[i])
        i+=1
    return (args,opts)

class usage:
    def __init__(self,use,mess,fmt):
        self.use = use
        self.mess = mess
        self.fmt = fmt

    def short(self):
        ret  = "Usage: "+self.use+"\n"
        ret += self.mess
        return ret

    def __str__(self):
        ret  = "Usage: "+self.use+"\n"
        ret += self.mess + "\n"
        ret += "\n"
        ret += "Options:\n"
        for i in self.fmt:
            ret += "\t %s, %s\t" % (i[0],i[1])
            if len(i) > 3:
                ret += i[3]
            ret += "\n"
        return ret

if __name__ == "__main__":
    argv = "neger --set lel wat is --be deze --het werkt".split(" ")
    opts = [("s","set",1),("b","be",0),("h","het",1)]
    print "input is",' '.join(argv)
    print "options zijn"
    for opt in opts:
        print "\t",opt[0],opt[1],opt[2]
    ret = parse_args(argv,opts)
    print "Arguments:",' '.join(ret[0])
    for i in ret[1]:
        print "\t"+' '.join(i)
    
