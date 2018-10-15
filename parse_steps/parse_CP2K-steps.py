#!/usr/bin/env python3

# Tested for 'PRINT_LEVEL MEDIUM' and MD_NVT

import argparse
from argparse import RawTextHelpFormatter #needed to go next line in the help text

######## agparse section
parser = argparse.ArgumentParser(description="Program to read CP2K's output", formatter_class=RawTextHelpFormatter)

parser.add_argument("cp2koutput",
                      type=str,
                      help="path to the output file to read\n")

args = parser.parse_args()

num_lines = sum(1 for line in open(args.cp2koutput))

file = open(args.cp2koutput, 'r')
print('#step energy dispersion pressure cell_vol cell_a cell_b cell_c cell_alp cell_bet cell_gam max_step rms_step max_grad rms_grad')
runtype='still_unknown'
step=0
pressure=0.0
max_step=0.0
rms_step=0.0
max_grad=0.0
rms_grad=0.0

for i in range(num_lines):
  print_now=False
  line=file.readline().split()
  if len(line)==4 and line[0]=='GLOBAL|' and line[1]=='Run' and line[2]=='type':  runtype=line[3]

  if len(line)>0 and line[0]=='CELL|':
     if len(line)==4  and line[1]=='Volume':    cell_vol=float(line[3])
     if len(line)==10 and line[2]=='a':         cell_a=float(line[9])
     if len(line)==10 and line[2]=='b':         cell_b=float(line[9])
     if len(line)==10 and line[2]=='c':         cell_c=float(line[9])
     if len(line)==6  and line[3]=='alpha':     cell_alp=float(line[5])
     if len(line)==6  and line[3]=='beta':      cell_bet=float(line[5])
     if len(line)==6  and line[3]=='gamma':     cell_gam=float(line[5])

  if len(line)==3 and line[0]=='Dispersion'   and line[1]=='energy:':        		            dispersion=float(line[2])
  if len(line)==9 and line[0]=='ENERGY|'      and line[1]=='Total':        		                energy=float(line[8])

  if runtype=='ENERGY':
      if i==(num_lines-1):                                                                          print_now=True

  if runtype=='GEO_OPT' or runtype=='CELL_OPT':
      if len(line)==7 and line[1]=='Informations' and line[3]=='step':   		                    step=int(line[5])
      if len(line)==5 and line[0]=='Max.'         and line[1]=='step'      and line[2]=='size':     max_step=float(line[4])
      if len(line)==5 and line[0]=='RMS'          and line[1]=='step'      and line[2]=='size': 	rms_step=float(line[4])
      if len(line)==4 and line[0]=='Max.'         and line[1]=='gradient':  			            max_grad=float(line[3])
      if len(line)==4 and line[0]=='RMS'          and line[1]=='gradient':  			            rms_grad=float(line[3])
      if len(line)==1 and line[0]=='---------------------------------------------------':           print_now=True

  if runtype=='CELL_OPT':
      if len(line)==5 and line[0]=='Internal'     and line[1]=='Pressure':   		                pressure=float(line[4])

  if runtype=='MD':
      if len(line)==4 and line[0]=='STEP'        and line[1]=='NUMBER':   		                    step=int(line[3])
      if len(line)==4 and line[0]=='INITIAL'     and line[1]=='PRESSURE[bar]':                      pressure=float(line[3]); print_now=True
      if len(line)==5 and line[0]=='PRESSURE'    and line[1]=='[bar]':                              pressure=float(line[3]); print_now=True

  if print_now: print('%d %.4f %.4f %.1f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.4f %.4f %.4f %.4f' \
                    %(step,energy,dispersion,pressure,\
                      cell_vol,cell_a,cell_b,cell_c,cell_alp,cell_bet,cell_gam,
                      max_step,rms_step,max_grad,rms_grad))
