import matplotlib.pyplot as plt
import math

initial_hcl_conc = 0.1 #M
initial_hcl_volume = 0.02 #L (20mL)
naoh_conc = 0.1

precision = 0.001
hcl_conc = initial_hcl_conc
ph = -math.log10(hcl_conc)
hcl_volume = initial_hcl_volume
total_volume = initial_hcl_volume
naoh_added = 0
naoh_remaining = 0.04

x = []
y = []

while naoh_added <= 0.02:
    naoh_added += precision
    hcl_mol = hcl_conc * total_volume
    total_volume += precision
    hcl_mol -= naoh_conc * precision
    if(hcl_mol < 0):
        continue
    hcl_conc = hcl_mol / total_volume
    ph = -math.log10(hcl_conc)
    x.append(naoh_added)
    y.append(ph)
    print(x,y)