def print_steps_header():
    print('step,energy(Ha),energy(eV/atom),dispersion(eV/atom),pressure(bar),cell_vol(A^3),'+\
          'cell_a(A),cell_b(A),cell_c(A),cell_alp(deg),cell_bet(deg),cell_gam(deg),'+\
          'max_dr(bohr),rms_dr(bohr),max_grad(Ha/bohr),rms_grad(Ha/bohr)')

def print_steps(cp2koutfile):
    BOHR2ANG = 0.529177208590000
    HA2EV = 27.211
    file = open(cp2koutfile, 'r')
    runtype='still_unknown'
    natoms=0
    step=0
    energy = None
    dispersion=0.0 #Needed if no dispersions are included
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
          if len(data)==5 and data[0]=='Internal'    and data[1]=='Pressure':   	pressure=float(data[4])
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
          print('%d,%.5f,%.5f,%.5f,%.1f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.3f,%.4f,%.4f,%.4f,%.4f' \
              %(step,energy,energy*HA2EV/natoms,dispersion*HA2EV/natoms,pressure,
                cell_vol,cell_a,cell_b,cell_c,cell_alp,cell_bet,cell_gam,
                max_step,rms_step,max_grad,rms_grad))
      if len(line)==0:
          if energy==None:
              print(" *** WARNING: CALCULATION CRASHED before the first step *** ")
          break
    file.close()

def parse_bandgap(cp2koutfile):
    '''Given a cp2k.out file where the band gap is compute, returns alpha and beta bandgap.
    This is parsed when the &MO_CUBES is activated with one NLUMO.
    (Note that &MO prints one energy per line and also the occupation but does not work with OT)
    Note: orbitals with occupation > 0.000 are considered as occupied!
    '''
    import numpy as np
    import re
    HA2EV = 27.211

    info = { 'uks' : False,
             'smearing' : False,
             'bg_alpha' : None,
             'bg_beta'  : None,
             'nel_alpha' : None, #Number of electrons
             'nel_beta' : None,
             'eigen_alpha' : np.array([]),
             'eigen_beta' :  np.array([]),
             }

    file = open(cp2koutfile, "r")
    read_eigen = False

    for line in file:
        if re.search('Kohn-Sham calculation', line):
            if line.split()[-1] == 'UKS':
                info['uks'] = True

        if re.search('Smear method', line):
            info['smearing'] = True

        if re.search('Number of electrons: ', line): # found at every opt step
            if info['nel_alpha'] == None:
                info['nel_alpha'] = int(line.split()[3])
            elif info['uks'] and info['nel_beta'] == None:
                info['nel_beta'] = int(line.split()[3])
        # If one of this expressions is found, start to read values
        #          Eigenvalues of the occupied subspace spin            1
        # Lowest eigenvalues of the unoccupied subspace spin            1
        if  re.search("subspace spin", line) and int(line.split()[-1]) == 1:
            read_eigen = 'eigen_alpha'
            continue
        elif re.search("subspace spin", line) and int(line.split()[-1]) == 2:
            read_eigen = 'eigen_beta'
            continue

        if read_eigen:
            if re.search("-------------", line) or re.search("Reached convergence", line):
                continue
            if len(line.split()) > 0 and len(line.split()) <= 4:
                info[read_eigen] = np.append(info[read_eigen], line.split())
                info[read_eigen] = info[read_eigen].astype(np.float)
            else:
                read_eigen = False
    if info['uks'] == False:
        i = int(info['nel_alpha']/2) # index of the LUMO
        info['bg_alpha'] = (info["eigen_alpha"][i] - info["eigen_alpha"][i-1])*HA2EV
    else:
        i = info['nel_alpha'] # index of the LUMO
        info['bg_alpha'] = (info["eigen_alpha"][i] - info["eigen_alpha"][i-1])*HA2EV
        i = info['nel_beta'] # index of the LUMO
        info['bg_beta'] = (info["eigen_beta"][i] - info["eigen_beta"][i-1])*HA2EV

    return info

def print_bandgap_header():
    print('Smearing,BG_alpha(eV),BG_beta(eV),N_electrons_alpha,N_electrons_beta')

def print_bandgap(info):
    if info['uks']:
        print('%r,%.3f,%.3f,%d,%d' \
              %(info['smearing'] ,
                info['bg_alpha'],
                info['bg_beta'],
                info['nel_alpha'],
                info['nel_beta']
                ))
    else:
        print('%r,%.3f,None,%d,None' \
              %(info['smearing'],
                info['bg_alpha'],
                info['nel_alpha']
                ))
