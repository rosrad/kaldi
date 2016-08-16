#!/usr/bin/env python
import sys
import kaldi_io

def compute_error(reg, ref, offset=6):
    reg_dict={k:v for k,v in kaldi_io.read_vec_int_ark(reg)}
    keys=reg_dict.keys()
    num_err=0
    for k,v in kaldi_io.read_vec_int_ark(ref):
        if k in keys:
            num_err+=abs(v-reg_dict[k])>offset

    return float(num_err)/len(keys)        


def main():
    narg=len(sys.argv);
    if narg < 3:
        print "No enough parameters"
        print "compute_er.py reg ref"
        sys.exit()
    if narg <4:
        offset=30;
    else:
        offset=sys.argv[3];

    reg = sys.argv[1];
    ref = sys.argv[2];
    offset=offset/5;
    print compute_error(reg, ref, offset)

if __name__ == '__main__':
    main()
