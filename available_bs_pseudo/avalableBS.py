#!/usr/bin/env python3

import string,sys
import numpy
import math
import subprocess
import argparse
from argparse import RawTextHelpFormatter #needed to go next line in the help text
import os
import re                                 #re.split('(\d+)',"O23") = ['O', '23', '']
from atomic_data import *

parser = argparse.ArgumentParser(description='Program to read, extract info and convert crystal files (by Daniele Ongari)', formatter_class=RawTextHelpFormatter)

parser.add_argument("-i","--inputfile",
                      action="store",
                      type=str,
                      dest="inputfile",
                      default="BASIS_MOLOPT_UCL",
                      help="path to the input file to read\n"+
                           "IMPLEMENTED: xyz(w/CELL),pdb,cssr,pwi,pwo,cif,xsf,axsf,subsys(CP2K),\n"+
                           "             restart(CP2K),inp(CP2K),cube,POSCAR(VASP) \n"+
                           "             [NEXT: gaussian, dcd+atoms,POSCAR(VASP)]")

parser.add_argument("-o","--output",
                      action="store",
                      type=str,
                      dest="output",
                      default=None,
                      help="Output filename.extension or just the extension\n"+
                           "IMPLEMENTED: cif,pdb,cssr,xyz(w/CELL),pwi,subsys(CP2K),axsf,geo(GULP)")


args = parser.parse_args()


#reading input file: name and format (notice that if there is a path it becomes part of the name, to have the output in the same place)
if not os.path.isfile(args.inputfile): sys.exit("ERROR: The file %s doesn't exist!" %args.inputfile)

for an in range(1, len(atomic_symbol)):
    at=atomic_symbol[an]
    print(at)
    file = open(args.inputfile, "r")
    countline=0
    for line in file:
        if re.search(" "+at+"  ", line) or re.search("^"+at+" ", line): #for BASIS_MOLOPT and BASIS_MOLOPT_UCL
            bs=line.split()[-1]
            file1 = open(args.inputfile, "r")
            largestcoeff=float(file1.readlines()[countline+3].split()[0])
            print("%s %.1f"%(bs,largestcoeff))
        countline+=1
