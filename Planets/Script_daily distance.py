import numpy as np
import matplotlib.pyplot as plt


R_V = 108.2 # million km
R_E = 149.6 # million km
R_M = 228.0 # million km
ratio_V = R_V / R_E
ratio_M = R_M / R_E
pi2 = 2*np.pi
t_unit = 1 # (in number of days)
# time unit = 32 days, to interpolate daily values (1 obs ever 32 day)
omega_V = t_unit * pi2 / 224.7 # angular velocity per 32 days
omega_E = t_unit * pi2 / 365.2 # angular velocity per 32 days
omega_M = t_unit * pi2 / 687.0 # angular velocity per 32 days
time = []
d_V = []
d_M = []
d_sum = []
t_incr = 1 # (in number of days)
T = 365 * 10 # time period (in number of days)
OUT = open("gt_distances.txt","w")
for t in np.arange(0, T, t_incr):
    time.append(t)
    dist_V = R_E * np.sqrt(1 + ratio_V**2 - 2*ratio_V * np.cos((omega_V - omega_E)*t))
    dist_M = R_E * np.sqrt(1 + ratio_M**2 - 2*ratio_M * np.cos((omega_M - omega_E)*t))
    d_V.append(dist_V)
    d_M.append(dist_M)
    d_sum.append(dist_V + dist_M) # near absolute minimum every ˜ 400 years
    OUT.write(str(dist_V + dist_M)+"\n")
OUT.close()
plt.plot(time,d_V)
plt.plot(time,d_M)
plt.plot(time,d_sum,c="green")
plt.show()