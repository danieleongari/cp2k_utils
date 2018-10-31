#!/usr/bin/env python3

from parser_utils import print_header, print_steps

# Tested for 'PRINT_LEVEL MEDIUM' and MD_NVT

import argparse
from argparse import RawTextHelpFormatter #needed to go next line in the help text

######## agparse section
parser = argparse.ArgumentParser(description="Program to read CP2K's output", formatter_class=RawTextHelpFormatter)

parser.add_argument("cp2koutput",
                      type=str,
                      help="path to the output file to read\n")

args = parser.parse_args()

print_header()
print_steps(args.cp2koutput)
