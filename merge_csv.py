#! /usr/bin/env python3
'''
Merge HIV-TRACE CSVs from multiple jurisdictions
'''

# imports
from csv import reader, writer
from gzip import open as gopen
from os.path import isfile
from sys import argv, stderr
import argparse

# constants
HIVTRACE_MERGE_CSV_VERSION = '0.0.1'
UNIQUE_ID_FIELDS = ['ehars_uid', 'SequenceID_predq', 'predq_clean_seq'] # fields to uniquely ID a sequence
HEADER = None # will be overwritten by first loaded CSV

# parse user args
def parse_args():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output_csv', required=False, type=str, default='stdout', help="Output Merged CSV")
    parser.add_argument('csv', nargs='+', type=str, help="Input CSV")
    args = parser.parse_args()
    args.csv = set(args.csv)
    if len(args.csv) < 2:
        raise ValueError("Must specify at least 2 input CSV files")
    for fn in args.csv:
        if not isfile(fn):
            raise ValueError("File not found: %s" % fn)
    if isfile(args.output_csv) and fn != 'stdout':
        raise ValueError("Output file exists: %s" % fn)
    return args

# load sequence data from CSV
def load_csv(fn):
    if fn.strip().lower().endswith('.gz'):
        f = gopen(fn, 'rt')
    else:
        f = open(fn, 'rt')
    data = dict() # same structure as `data` in `main()`
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
    f.close()
    return data

# main script logic
def main():
    args = parse_args()
    data = dict() # data[unique_seq_ID] = dict mapping column headers to values
    for fn in args.csv:
        curr_data = load_csv(fn)
        for unique_seq_ID, unique_seq_vals in curr_data.items():
            if unique_seq_ID in data:
                existing_vals = data[unique_seq_ID]
                if unique_seq_vals['hiv_aids_dx_dt'] < existing_vals['hiv_aids_dx_dt']:
                    existing_vals['hiv_aids_dx_dt'] = unique_seq_vals['hiv_aids_dx_dt']
            else:
                data[unique_seq_ID] = unique_seq_vals
    if args.output_csv.strip().lower().endswith('.gz'):
        f = gopen(args.output_csv, 'wt')
    else:
        f = open(args.output_csv, 'wt')
    csv_writer = writer(f)
    csv_writer.writerow(HEADER)
    for unique_seq_vals in data.values():
        csv_writer.writerow([unique_seq_vals[name] for name in HEADER])
    f.close()

# run script
if __name__ == "__main__":
    main()
