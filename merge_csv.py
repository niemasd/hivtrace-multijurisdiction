#! /usr/bin/env python3
'''
Merge HIV-TRACE CSVs from multiple jurisdictions
'''

# imports
from csv import reader
from gzip import open as gopen
from os.path import isfile
from sys import argv, stderr
import argparse

# constants
HIVTRACE_MERGE_CSV_VERSION = '0.0.1'
UNIQUE_ID_FIELDS = ['ehars_uid', 'SequenceID_predq', 'predq_clean_seq'] # fields to uniquely ID a sequence

# parse user args
def parse_args
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-o', '--output_csv', required=False, type=str, default='stdout', help="Output Merged CSV")
    parser.add_argument('csv', required=True, nargs='+', type=str, help="Input CSV")
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

# main script logic
def main():
    args = parse_args()

# run script
if __name__ == "__main__":
    main()
