#!/usr/bin/env python3

from parser_utils import print_steps_header, print_steps
from parser_utils import parse_bandgap, print_bandgap_header, print_bandgap

# Tested for 'PRINT_LEVEL MEDIUM' and MD_NVT

import argparse
from argparse import RawTextHelpFormatter #needed to go next line in the help text

######## agparse section
parser = argparse.ArgumentParser(description="Program to read CP2K's output", formatter_class=RawTextHelpFormatter)

parser.add_argument("parse",
                    type=str,
                    choices=["steps","bandgap"],
                    help="Choice of what to parse")

parser.add_argument("cp2koutput",
                    type=str,
                    help="Path to the output file to read")

args = parser.parse_args()

if args.parse=="steps":
    print_steps_header()
    print_steps(args.cp2koutput)

if args.parse=="bandgap":
    print_bandgap_header()
    bandgap_info = parse_bandgap(args.cp2koutput)
    print_bandgap(bandgap_info)
