def print_header():
    print('#step energy(eV/atom) energy(Ha) dispersion(Ha) pressure(bar) cell_vol(A^3) '+\
          'cell_a(A) cell_b(A) cell_c(A) cell_alp(deg) cell_bet(deg) cell_gam(deg) '+\
          'max_dr(bohr) rms_dr(bohr) max_grad(Ha/bohr) rms_grad(Ha/bohr)')

def print_steps(cp2kfile):
    BOHR2ANG = 0.529177208590000
    HA2EV = 27.211
    file = open(cp2kfile, 'r')
    runtype='still_unknown'
    natoms=0
    step=0
    energy = None
    pressure=0.0
    max_step=0.0
    rms_step=0.0
    max_grad=0.0
    rms_grad=0.0

    while True:
      print_now=False
      line=file.readline()
      data= line.split()
      # General info
      if len(data)==4 and data[0]=='GLOBAL|' and data[1]=='Run' and data[2]=='type': runtype=data[3]
      if len(data)==3 and data[0]=='-' and data[1]=='Atoms:': natoms=int(data[2])
      if runtype=='MD' and len(data)==4 and data[1]=='Ensemble':
          if  data[3]=='NVT':
              runtype='MD-NVT'
          elif data[3]=='NPT_F':
              runtype='MD-NPT_F'

      if len(data)>0 and data[0]=='CELL|':
         if len(data)==4  and data[1]=='Volume':    cell_vol=float(data[3])
         if len(data)==10 and data[2]=='a':         cell_a=float(data[9])
         if len(data)==10 and data[2]=='b':         cell_b=float(data[9])
         if len(data)==10 and data[2]=='c':         cell_c=float(data[9])
         if len(data)==6  and data[3]=='alpha':     cell_alp=float(data[5])
         if len(data)==6  and data[3]=='beta':      cell_bet=float(data[5])
         if len(data)==6  and data[3]=='gamma':     cell_gam=float(data[5])
      if len(data)==3 and data[0]=='Dispersion'   and data[1]=='energy:':        		            dispersion=float(data[2])
      if len(data)==9 and data[0]=='ENERGY|'      and data[1]=='Total':        		                energy=float(data[8])
      # Specific info
      if runtype=='ENERGY':
          if len(line)==0: print_now=True
      if runtype in ['GEO_OPT','CELL_OPT']:
          if len(data)==7 and data[1]=='Informations' and data[3]=='step':   		                    step=int(data[5])
          if len(data)==5 and data[0]=='Max.'         and data[1]=='step'      and data[2]=='size':     max_step=float(data[4])
          if len(data)==5 and data[0]=='RMS'          and data[1]=='step'      and data[2]=='size': 	rms_step=float(data[4])
          if len(data)==4 and data[0]=='Max.'         and data[1]=='gradient':  			            max_grad=float(data[3])
          if len(data)==4 and data[0]=='RMS'          and data[1]=='gradient':  			            rms_grad=float(data[3])
          if len(data)==1 and data[0]=='---------------------------------------------------':           print_now=True
          #Note: with CELL_OPT/LBFGS there is no "STEP 0", while there is with CELL_OPT/BFGS
      if runtype=='CELL_OPT':
          if len(data)==5 and data[0]=='Internal'     and data[1]=='Pressure':   	pressure=float(data[4])
      if runtype =='MD-NVT':
          if len(data)==4 and data[0]=='STEP'        and data[1]=='NUMBER':   		step=int(data[3])
          if len(data)==4 and data[0]=='INITIAL'     and data[1]=='PRESSURE[bar]':  pressure=float(data[3]); print_now=True
          if len(data)==5 and data[0]=='PRESSURE'    and data[1]=='[bar]':          pressure=float(data[3]); print_now=True
      if runtype=='MD-NPT_F':
          if len(data)==4 and data[0]=='STEP'        and data[1]=='NUMBER':   		step=int(data[3])
          if len(data)==4 and data[0]=='INITIAL'     and data[1]=='PRESSURE[bar]':  pressure=float(data[3]); print_now=True
          if len(data)==5 and data[0]=='PRESSURE'    and data[1]=='[bar]':          pressure=float(data[3]);
          if len(data)==4 and data[0]=='VOLUME[bohr^3]':                            cell_vol=float(data[3])*(BOHR2ANG**3)
          if len(data)==6 and data[1]=='LNTHS[bohr]':
                                                                                    cell_a=float(data[3])*BOHR2ANG
                                                                                    cell_b=float(data[4])*BOHR2ANG
                                                                                    cell_c=float(data[5])*BOHR2ANG
          if len(data)==6 and data[1]=='ANGLS[deg]':
                                                                                    cell_alp=float(data[3])
                                                                                    cell_bet=float(data[4])
                                                                                    cell_gam=float(data[5])
                                                                                    print_now=True
      # Print step, print warning if the end of the file came but no ener
      if print_now and energy != None:
          print('%d %.4f %.4f %.4f %.1f %.3f %.3f %.3f %.3f %.3f %.3f %.3f %.4f %.4f %.4f %.4f' \
              %(step,energy*HA2EV/natoms,energy,dispersion,pressure,\
                cell_vol,cell_a,cell_b,cell_c,cell_alp,cell_bet,cell_gam,
                max_step,rms_step,max_grad,rms_grad))
      if len(line)==0:
          if energy==None:
              print(" *** WARNING: CALCULATION CRASHED before the first step *** ")
          break
    file.close()
