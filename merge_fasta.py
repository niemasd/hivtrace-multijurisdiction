#! /usr/bin/env python3
'''
Merge aligned FASTAs (i.e., what gets fed to TN93) from multiple jurisdictions
'''

# imports
from gzip import open as gopen
from json import dump as jdump
from os.path import isfile
from sys import argv, stderr
import argparse

# constants
HIVTRACE_MERGE_FASTA_VERSION = '0.0.1'

# open a file for reading/writing
def open_file(fn, mode='rt'):
    if fn == 'stdin':
        from sys import stdin as f
    elif fn == 'stdout':
        from sys import stdout as f
    elif fn == 'stderr':
        from sys import stderr as f
    elif fn.strip().lower().endswith('.gz'):
        f = gopen(fn, mode=mode)
    else:
        f = open(fn, mode=mode)
    return f

# parse user args
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-of', '--output_fasta', required=True, type=str, help="Output Merged FASTA")
    parser.add_argument('-oj', '--output_json', required=True, type=str, help="Output Info JSON")
    parser.add_argument('fasta', nargs='+', type=str, help="Input FASTA")
    args = parser.parse_args()
    args.fasta = set(args.fasta)
    if len(args.fasta) < 2:
        raise ValueError("Must specify at least 2 input FASTA files")
    for fn in args.fasta:
        if not isfile(fn):
            raise ValueError("File not found: %s" % fn)
    for fn in [args.output_fasta, args.output_json]:
        if isfile(fn):
            raise ValueError("Output file exists: %s" % fn)
    return args

# load sequence data from FASTA
def load_fasta(fasta_fn):
    data = dict() # same structure as `data` in `main()`
    with open_file(fasta_fn, 'rt') as f:
        lines = [l.strip() for l in f]
        data = {(lines[i][1:], lines[i+1]) for i in range(0, len(lines), 2)}
    return data

# main script logic
def main():
    # set things up
    args = parse_args()
    data = set() # set of (fasta_ID, seq) tuples
    access = dict() # access[fasta_fn] = set of (fasta_ID, seq) tuples this jurisdiction has access to

    # load data from FASTAs
    for fasta_fn in args.fasta:
        curr_data = load_fasta(fasta_fn)
        access[fasta_fn] = list(curr_data) # JSON can't serialize set
        data |= curr_data

    # write output merged FASTA
    with open_file(args.output_fasta, 'wt') as f:
        for fasta_tuple in data:
            f.write('>%s\n%s\n' % fasta_tuple)

    # write output info JSON
    info = {
        'access': access, # which input files have access to which unique sequence IDs
    }
    with open_file(args.output_json, 'wt') as f:
        jdump(info, f)

# run script
if __name__ == "__main__":
    main()
