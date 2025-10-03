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
UNIQUE_ID_FIELDS = ['ehars_uid', 'SequenceID_predq', 'predq_clean_seq'] # fields to uniquely ID a sequence

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
        print('\n'.join(lines[:2])); exit() # TODO STORE SEQS IN DATA DICT, WHERE KEYS ARE UNIQUE SEQ TUPLES (NOT FASTA IDs)
        for row_num, row in enumerate(reader(f)):
            if row_num == 0: # header
                header = [s.strip() for s in row]
                name2ind = {name:ind for ind, name in enumerate(header)}
                global HEADER
                if HEADER is None:
                    HEADER = header
            else:
                unique_seq_ID = tuple(row[name2ind[name]] for name in UNIQUE_ID_FIELDS)
                if unique_seq_ID in data:
                    pass # TODO handle duplicate sequences in single jurisdiction's CSV (currently ignore all but first)
                else:
                    data[unique_seq_ID] = {header[ind]:val for ind, val in enumerate(row)}
    return data

# main script logic
def main():
    # set things up
    args = parse_args()
    data = dict() # data[unique_seq_ID] = dict mapping column headers to values
    access = dict() # access[csv_fn] = set of unique_seq_ID tuples this jurisdiction has access to

    # load data from FASTAs
    for fasta_fn in args.fasta:
        curr_data = load_fasta(fasta_fn)
        raise NotImplementedError("TODO CONTINUE HERE")
        access[csv_fn] = list(curr_data.keys())
        for unique_seq_ID, unique_seq_vals in curr_data.items():
            if unique_seq_ID in data:
                existing_vals = data[unique_seq_ID]
                if unique_seq_vals['hiv_aids_dx_dt'] < existing_vals['hiv_aids_dx_dt']:
                    existing_vals['hiv_aids_dx_dt'] = unique_seq_vals['hiv_aids_dx_dt']
            else:
                data[unique_seq_ID] = unique_seq_vals

    # write output merged CSV
    with open_file(args.output_csv, 'wt') as f:
        csv_writer = writer(f)
        csv_writer.writerow(HEADER)
        for unique_seq_vals in data.values():
            csv_writer.writerow([unique_seq_vals[name] for name in HEADER])

    # write output info JSON
    info = {
        'unique_seq_ID_fields': UNIQUE_ID_FIELDS, # fields to define a "unique" sequence
        'access': access,                         # which input files have access to which unique sequence IDs
    }
    with open_file(args.output_json, 'wt') as f:
        jdump(info, f)

# run script
if __name__ == "__main__":
    main()
