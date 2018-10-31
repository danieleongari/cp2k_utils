''' 
Simple programs that reads the cp2k.out and prints for each atom the atomic number and the core electrons,
as needed for the chargemol program to compute DDEC charges.
If there are more kinds associated to the same element, these should have the same number of core electrons.
'''

file = open('./tests/cp2k_energy.out', 'r')

coredict={}

while True:
    line=file.readline().split()
    if len(line)==3 and line[0]=='-' and line[1]=='Atoms:':
        n_atoms=int(line[2])
    if len(line)==8 and line[0]=='Atom' and line[1]=='Kind' and line[2]=='Element':
        skip=file.readline()
        break
for a in range(n_atoms):
    line=file.readline().split()
    atom_number=int(line[3])
    atom_valence=int(float(line[7])) 
    atom_core=atom_number-atom_valence
    coredict.update({atom_number:atom_core})

for a in sorted(coredict):
    print("%d %d" %(a,coredict[a]))
