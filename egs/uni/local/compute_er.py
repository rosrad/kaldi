#!/usr/bin/env python
import sys
import kaldi_io
from optparse import OptionParser  


def collect_error(reg, ref, offset=6):
    reg_dict={k:v for k,v in kaldi_io.read_vec_int_ark(reg)}
    keys=reg_dict.keys()
    errors=[]
    for k,v in kaldi_io.read_vec_int_ark(ref):
        if k in keys:
            if abs(v-reg_dict[k])>offset:
                errors += [k]

    er = float(len(errors))/len(keys)
    return (er, errors)


def compute_error(reg, ref, offset=6):
    (er, errors) = collect_error(reg, ref, offset)
    return er

def main():
    parser = OptionParser()  
    parser.add_option("-c", "--collect-error", dest="collect",
                      action="store_true", default=False)

    (options, args) = parser.parse_args()  
    narg = len(args)
    if narg < 2:
        print "No enough parameters"
        print "compute_er.py [-options] reg ref"
        sys.exit()
    if narg < 3:
        offset=30;
    else:
        offset=args[2];

    reg = args[0];
    ref = args[1];
    offset=offset/5;
    (er,errors) = collect_error(reg,ref, offset)
    if options.collect:
        for k in errors:
            print k

    else:
        print er

if __name__ == '__main__':
    main()
