#!/usr/bin/env python3

import string
import sys
import numpy
import math
import subprocess
import argparse
from argparse import RawTextHelpFormatter #needed to go next line in the help text
import os
import re                                 #re.split('(\d+)',"O23") = ['O', '23', '']
from atomic_data import *

bs_types=('SZV-MOLOPT',
          'DZVP-MOLOPT',
          'TZVP-MOLOPT',
          'TZV2P-MOLOPT',
          'TZV2PX-MOLOPT',
          'SZV-MOLOPT-SR',
          'SZVP-MOLOPT-SR',
          'DZV-MOLOPT-SR',
          'DZVP-MOLOPT-SR',
          'DZVPd-MOLOPT-SR',
          'TZVP-MOLOPT-SR',
          'TZVPd-MOLOPT-SR',
          'TZV2P-MOLOPT-SR',
          'TZV2Pd-MOLOPT-SR')

tabgrid1=16
tabgrid2=16

# header
ofile=open('availableBS_specific.out', 'w')

print('atom-q\t'.expandtabs(tabgrid1),end='',file=ofile)
for bs in bs_types:
    print((bs+'\t').expandtabs(tabgrid2),end='',file=ofile)
print ('',file=ofile)
print ('',file=ofile)
# end header

collect_bs_types=[]

for an in range(1, len(atomic_symbol)):
    at=atomic_symbol[an]
    foundat=False
    for q in range(1,31):
      atqbsarray=[]
      foundatq=False
      for bs in bs_types:
          foundbs=False
          for inputfile in ['BASIS_MOLOPT','BASIS_MOLOPT_UCL']:
            file = open(inputfile, "r")
            countline=0
            for line in file:
                if (re.search(" "+at+" ",line) or re.search("^"+at+" ",line)) \
                and re.search(bs+"-GTH-q"+str(q)+"$",line):
                    foundat=True
                    foundatq=True
                    foundbs=True
                    if inputfile=='BASIS_MOLOPT'    : whichfile = 'ORG'
                    if inputfile=='BASIS_MOLOPT_UCL': whichfile = 'UCL'
                    file1 = open(inputfile, "r")
                    largestcoeff=float(file1.readlines()[countline+3].split()[0])
                    file1.close()
                countline+=1
            file.close()
          if not foundbs: atqbsarray.append('x')
          if foundbs:     atqbsarray.append(whichfile+"("+"{:.1f}".format(largestcoeff)+")")
      if foundatq:
          print((at+"-q"+str(q)+"\t").expandtabs(tabgrid1),end='',file=ofile)
          for i in atqbsarray:
              if i=='x': print (("x\t").expandtabs(tabgrid2),end='',file=ofile)
              else:      print ((i+"\t").expandtabs(tabgrid2),end='',file=ofile)
          print('',file=ofile,flush=True)
    if not foundat:
          print((at+"-NONE\t").expandtabs(tabgrid1),end='',file=ofile)
          for i in atqbsarray:
              print (("x\t").expandtabs(tabgrid2),end='',file=ofile)
          print('',file=ofile,flush=True)
