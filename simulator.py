# %% Import cell
import numpy as np
import matplotlib.pyplot as plt

# %% Pumps parameters
Qin = lambda t: 1  # m3/s and t is in sec
q = 10  # m3/s
Vmin = 10  # m3/s
Vmax = 10000  # m3/s

# %% Simulation parameters
deltaT = 1  # sec
T = 3600 * 24  # simulation time in sec

# %% Simulation
Nt = int(np.ceil(T / deltaT))

V = [Vmin]
ps = [0]  # which pump is active
for i in range(Nt - 1):
    t = i * deltaT
    if ps[-1] == 1:  # Pump 1 is active
        u = 1 if V[-1] >= Vmin else 0
    else:
        u = 1 if V[-1] >= Vmax else 0
    ps.append(u)
    Qout = q * u
    V.append(V[-1] + deltaT * (Qin(t) - Qout))

# %% Plot
fig, ax1 = plt.subplots()
t = np.linspace(0, T, Nt)

color = "tab:red"
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Pump active", color=color)
ax1.plot(t, ps, color=color)
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

color = "tab:blue"
ax2.set_ylabel("Volume [m^3]", color=color)  # we already handled the x-label with ax1
ax2.plot(t, V, color=color)
ax2.tick_params(axis="y", labelcolor=color)

plt.grid()

# %%
