import numpy as np
import matplotlib.pyplot as plt
run = ["default",
       "T-",
       "T+",
       "q-",
       "q+",
       "C-",
       "C+",
       "gammaT-",
       "gammaT+",
       "gammaq-",
       "gammaq+",
       "lat-",
       "lat+"
       ]
V = [14.258146074870929,
     14.232097162025825, 
     14.26555393603769, 
     14.25814989866569, 
     14.258143149670031,
     14.242632019517691,
     14.252987745651136, 
     14.266161565506037, 
     14.251383755999955, 
     14.257836349121133, 
     14.258488747071953, 
     14.228326349238289,
     14.260452144161501
      ]
iV = [156,
      156,
      156, 
      156,
      156,
      153,
      157,
      156,
      156,
      156,
      156,
      168,
      146
      ]


V = np.array(V, dtype=float)
iV = np.array(iV, dtype=float)
arr = np.column_stack([run, V, iV])
print(arr)

#diff
dV = V - V[0]
diV = iV - iV[0]
arrdif = np.column_stack([run, dV, diV])

print(arrdif)

runs = arr[:,0]
V_vals = arr[:,1].astype(float)
iV_vals = arr[:,2].astype(float)

dV_vals = arrdif[:,1].astype(float)
diV_vals = arrdif[:,2].astype(float)

x = np.arange(len(runs))

# Plot 1: u und v
plt.figure(figsize=(9,4))
plt.plot(x, V_vals,marker='o', label='V')
plt.xticks(x, runs, rotation=45, ha='right')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Plot 2: Differenzenfor
plt.figure(figsize=(9,4))
plt.bar(x, dV_vals, label='V')
plt.axhline(0, color='k', lw=1)
plt.xticks(x, runs, rotation=45, ha='right')
plt.grid(alpha=0.3)
plt.legend()
plt.ylabel('Difference in V (m/s)')
plt.tight_layout()
plt.show()

# Plot 3: iu und iv
plt.figure(figsize=(9,4))
plt.plot(x, iV_vals, marker='o', label='t')
plt.xticks(x, runs, rotation=45, ha='right')
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.show()

# Plot 4: Differenzenfor
plt.figure(figsize=(9,4))
plt.bar(x, diV_vals, label='t')
plt.axhline(0, color='k', lw=1)
plt.xticks(x, runs, rotation=45, ha='right')
plt.grid(alpha=0.3)
plt.legend()
plt.ylabel('Difference in t (10 min)')
plt.tight_layout()
plt.show()