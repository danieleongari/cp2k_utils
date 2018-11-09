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

ft_types=('BLYP',
          'BP',
          'HCTH120',
          'HCTH407',
          'PADE',
          'PBE',
          'PBESOL',
          'OLYP')

tabgrid1=10
tabgrid2=10

# header
ofile=open('availablePOT_specific.out', 'w')

print('atom-q\t'.expandtabs(tabgrid1),end='',file=ofile)
for ft in ft_types:
    print((ft+'\t').expandtabs(tabgrid2),end='',file=ofile)
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
      for ft in ft_types:
          foundft=False
          file = open('GTH_POTENTIALS', "r")
          countline=0
          for line in file:
                if (                                                        \
                    re.search(" "+at+" ",line) or                           \
                    re.search("^"+at+" ",line)                              \
                   )                                                        \
                   and                                                      \
                   (                                                        \
                    re.search("GTH-"+ft+"-q"+str(q)+" ", line) or           \
                    re.search("GTH-"+ft+"-q"+str(q)+"\n",line)              \
                   ):
                    foundat=True
                    foundatq=True
                    foundft=True
                countline+=1
          file.close()
          if not foundft: atqbsarray.append('x')
          if foundft:     atqbsarray.append('AVAIL')
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
