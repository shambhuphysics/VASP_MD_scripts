import numpy as np
import matplotlib.pyplot as plt
with open('OUTCAR', 'r') as outcar, open('OSZICAR','r') as oszicar :
    outr=outcar.readlines()
    oscr=oszicar.readlines()
    T=[]
    P =[]
    E =[]
    for osr in oscr:
        if 'T=' in osr:
            T.append(float(osr.split()[2])) 
    for out in outr:
        if 'free  en' in out:
            E.append(float(out.split()[4]))
        elif 'total pressure' in out:
             P.append(float(out.split()[3])) 
print(f'<T> = {np.mean(T):.2f} K \n <P> = {np.mean(P)/10:.2f} GPa \n <E> ={np.mean(E):.2f} eV')
with open('README', 'w') as README :
     README.write(f'<T> = {np.mean(T):.2f} K \n <P> = {np.mean(P)/10:.2f} GPa \n <E> ={np.mean(E):.2f} eV')
    
fig, axes = plt.subplots(3, 1, figsize=(6, 6))
axes[0].plot(T)
axes[1].plot(P)
axes[2].plot(E)
plt.show()
