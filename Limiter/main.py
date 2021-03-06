import numpy as np
import matplotlib.pyplot as plt

# Defining Input Signal
fs = 8000 # sampling rate
Ts = 1/fs # sampling period

# Defining three sinusoids to be played consecutively
A1 = 2 # Amplitude of first sinusoid
f1 = 300 # f1 = 0.3 kHz
t1 = np.arange(0,0.025,Ts) # t1 from 0 to 25 msec
A2 = 4 # Amplitude of second sinusoid
f2 = 600 # f2 = 0.6 kHz
t2 = np.arange(0.025,0.05,Ts)   # t2 from 25 msec to 50 msec
A3 = 0.5 # Amplitude of third sinusoid
f3 = 1200 # f3 = 1.2 kHz
t3 = np.arange(0.05, 0.075, Ts) # t3 from 50 msec to 75 msec
x = np.concatenate([A1*np.cos(2*np.pi*f1*t1), A2*np.cos(2*np.pi*f2*t2), A3*np.cos(2*np.pi*f3*t3)])

# Create envelope for plotting
envInTop = np.array([A1]*200 + [A2]*200 + [A3]*200)
envInBot = envInTop * -1
t = np.concatenate([t1, t2, t3])

# Plot input 
plt.plot(t*1000, x, t*1000, envInTop, '--g', t*1000, envInBot, '--g')
plt.axis([0, 75, -4.2, 4.2])
plt.legend('x(t)', 'envelope')
plt.text(60,3.5,'f_1 = 0.3 kHz')
plt.text(60,3.0,'f_2 = 0.6 kHz')
plt.text(60,2.5,'f_3 = 1.2 kHz')
plt.xlabel('t (msec)')
plt.title('input signal, x(t)')
plt.grid()
plt.show()

# Limiter Design
ta = 0.002 # attack time
tr = 0.01 # release time
Aa = np.exp(-2.3*Ts/ta) # attack forgetting factor
Ar = np.exp(-2.3*Ts/tr) #release forgetting factor
p = 1/100       # rho
c0 = 2.2        # threshold
g1 = 0          # for EMA gain-smoothing filter, g_n
g0 = 0          # g_[n-1]
c = 0           # Control signal
G = 0           #Smoothed gain
N = len(x)      # For limit on n

# Create empty lists for output and plotting output
y = cPlot = gPlot = GPlot = np.array([])
for n in range(N):
    if abs(x[n]) >= c:
        c = Aa*c + (1 - Aa)*abs(x[n])
    else:
        c = Ar*c + (1 - Ar)*abs(x[n])

    # For plotting
    cPlot = np.append(cPlot, c)

    g0 = g1

    if c == 0:
        g1 = 1
    elif c >= c0:
        g1 = (c/c0)**(p-1)
    else:
        g1 = 1
    
    gPlot = np.append(gPlot, g1)   # For plotting

    if g1 >= g0:     # EMA smoothing filter
        G = Aa*G + (1 - Aa)*g1
    else:
        G = Ar*G + (1 - Ar)*g1

    GPlot = np.append(GPlot, G)     # For plotting
    y = np.append(y, G*x[n])        # Output

# Normalize results
y = y/y.max()
m = max(y)      # Maximum value of y
for i in range(len(y)):
    y[i] = y[i]/m

# Plot Results
plt.subplot(2,2,1)
plt.plot(t*1000,y,t*1000,envInTop,'--g',t*1000,envInBot,'--g', t*1000, c0*np.ones(N),'--r',t*1000, -c0*np.ones(N),'--r')
plt.axis([0,75,-4.2,4.2])
plt.xlabel('t (msec)')
plt.title('limiter, y(t) = G(t)x(t)')
plt.text(60,3.4,'ρ = 1/3')
plt.grid()

plt.subplot(2,2,2)
plt.plot(t*1000,cPlot,'r',t*1000, c0*np.ones(N),'--b')
plt.axis([0,75,0,4])
plt.xlabel('t (msec)')
plt.title('control signal, c(t)'),
plt.legend('c(t)','c_0')
plt.grid()

plt.subplot(2,2,3)
plt.plot(t*1000,gPlot,'r')
plt.axis([0,75,0,1.2])
plt.xlabel('t (msec)')
plt.title('gain, g(t) = F(c(t))')
plt.grid()

plt.subplot(2,2,4)
plt.plot(t*1000,GPlot)
plt.axis([0,75,0,1.2])
plt.xlabel('t (msec)')
plt.title('smoothed gain, G(t)')
plt.grid()

plt.tight_layout()
plt.show()