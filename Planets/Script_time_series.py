# interpol_fourier.py (author: MLTechniques.com)
import numpy as np
import mpmath
import matplotlib as mpl
from matplotlib import pyplot as plt
import requests

# https://www.digitalocean.ie/Data/DownloadTideData

mode = 'Data' # options: 'Data', 'Math.Bessel', 'Math.Zeta'

#--- read data

raw_url = "https://raw.githubusercontent.com/VincentGranville/Statistical-Optimization/main/"
file = 'tides_Dublin.txt'
url = raw_url + file

# Fetch the file from the URL
response = requests.get(url)

if mode == 'Data':

    # one column: observed value
    # time is generated by the algorithm; integer for interpolation nodes

    # Read the content of the file line by line
    table = response.text.splitlines()

    temp={}
    t = 0
    # t/t_unit is an integer every t_unit observations (node)
    t_unit = 16 # use 16 for ocean tides, 32 for planet data discussed in the classroom
    for string in table:
        string = string.replace('\n', '')
        fields = string.split('\t')
        temp[t/t_unit] = float(fields[0])
        t = t + 1
    nobs = len(temp)

else:
    t_unit = 16

#--- function to interpolate

def g(t):
    if mode == 'Data':
        z = temp[t]
    elif mode == 'Math.Bessel':
        t = 40*(t-t_min)/(t_max-t_min)
        z = mpmath.besselj(1,t)
        z = float(z.real) # real part of the complex-valued function
    elif mode == 'Math.Zeta':
        t = 4 + 40*(t-t_min)/(t_max-t_min)
        z = mpmath.zeta(complex(0.5,t))
        z = float(z.real) # real part of the complex-valued function
    return(z)

#--- interpolation function

def interpolate(t, eps):
    sum = 0
    t_0 = int(t + 0.5) # closest interpolation node to t
    pi2 = 2/np.pi
    flag1 = -1
    flag2 = -1
    for k in range(0, n):
        # use nodes k1, k2 in interpolation formula
        k1 = t_0 + k
        k2 = t_0 - k
        tt = t - t_0
        if k != 0:
            if k %2 == 0:
                z = g(k1) + g(k2)
                if abs(tt**2 - k**2) > eps:
                    term = flag1 * tt*z*pi2 * np.sin(tt/pi2) / (tt**2 - k**2)
                else:
                    # use limit as tt --> k
                    term = z/2
                flag1 = -flag1
            else:
                z = g(k1) - g(k2)
                if abs(tt**2 - k**2) > eps:
                    term = flag2 * tt*z*pi2 * np.cos(tt/pi2) / (tt**2 - k**2)
                else:
                    # use limit as tt --> k
                    term = z/2
                flag2 = -flag2
        else:
            z = g(k1)
            if abs(tt) > eps:
                term = z*pi2*np.sin(tt/pi2) / tt
            else:
                # use limit as tt --> k (here k = 0)
                term = z
        sum += term
    return(sum)

#--- main loop and visualizations

n  = 8
    # 2n+1 is number of nodes used in interpolation
    # in all 3 cases tested (data, math functions), n >= 8 works
if mode=='Data':
    # restrictions:
    #     t_min >= n, t_max  <= int(nobs/t_unit - n)
    #     t_max > t_min, at least one node between t_min and t_max
    t_min  = n  # interpolate between t_min and t_max
    t_max  = int(nobs/t_unit - n)  # must have t_max - t_min > 0
else:
    t_min = 0
    t_max = 100
incr   = 1/t_unit   # time increment between nodes
eps    = 1.0e-12

OUT = open("interpol_tides_Dublin.txt","w")

time = []
ze = []
zi = []

fig = plt.figure(figsize=(6,3))
mpl.rcParams['axes.linewidth'] = 0.2
mpl.rc('xtick', labelsize=6)
mpl.rc('ytick', labelsize=6)

for t in np.arange(t_min, t_max, incr):
    time.append(t)
    z_interpol = interpolate(t, eps)
    z_exact = g(t)
    zi.append(z_interpol)
    ze.append(z_exact)
    error = abs(z_exact - z_interpol)
    if t == int(t):
        plt.scatter(t,z_exact,color='orange', s=6)
    print("t = %8.5f exact = %8.5f interpolated = %8.5f error = %8.5f %3d nodes" % (t,z_exact,z_interpol,error,n))
    OUT.write("%10.6f\t%10.6f\t%10.6f\t%10.6f\n" % (t,z_exact,z_interpol,error))
OUT.close()

plt.plot(time,ze,color='red',linewidth = 0.5, alpha=0.5)
plt.plot(time,zi,color='blue', linewidth = 0.5,alpha=0.5)
base = min(ze) - (max(ze) -min(ze))/10
for index in range(len(time)):
    # plot error bars showing delta between exact and interpolated values
    t = time[index]
    error = abs(zi[index]-ze[index])
    plt.vlines(t,base,base+error,color='black',linewidth=0.2)
plt.savefig('tides2.png', dpi=200)
plt.show()