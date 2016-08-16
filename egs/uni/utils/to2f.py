#!/usr/bin/env python
import sys
import re



def to2f(m):
    return "%.2f"%float(m.group())

def main():
    narg = len(sys.argv)
    if narg < 3:
        print "no enough args!"
        print "usage : %s input output"%sys.argv[0]
        return

    input = sys.argv[1]
    output = sys.argv[2]

    p = re.compile(r'\d+\.\d+')
    with open(output, 'wb') as wf:
        for l in open(input, 'rb'):
            wf.write(p.sub(to2f,l))

if __name__ == '__main__':
    main()
