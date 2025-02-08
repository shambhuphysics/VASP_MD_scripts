import numpy as np
import matplotlib.pyplot as plt
print( 'THE INFORMATION FROM OUTCAR!!')
with open('OUTCAR', 'r') as outcar, open ('CONTCAR','r') as  contcar :
    outr=outcar.readlines()
    contr =contcar.readlines()
    print(f' =======================================')
    [print(line.strip()) for line in lines[11:30]]
    print(f' =======================================')
    for out in outr:
        if 'energy-cutoff' in out:
            print(f' The Energy-cutoff: { out.split()[2]} eV')
            break
        elif 'volume of cell :' in out:
            print(f' Volume of cell: { out.split()[4]} ')
        elif 'generate k-points for:' in out:
            print(f' KPOINTS used: {out.split()[3]} x {out.split()[4]} x {out.split()[5]} ')
    print(f' Total number of atoms used:{contr[6]}')
