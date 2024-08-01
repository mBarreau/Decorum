# %% Import cell
import numpy as np
import matplotlib.pyplot as plt

# %% Pumps parameters
Qin = lambda t: 5 - 1 * np.cos(2 * np.pi * t / (3600 * 24))  # m3/s and t is in sec
q = [10, 5, 10]  # m3/s
Vmin = 10  # m3/s
Vmax = 10000  # m3/s

# %% Simulation parameters
deltaT = 1  # sec
T = 3600 * 24  # simulation time in sec

# %% Simulation
Nt = int(np.ceil(T / deltaT))
Npumps = len(q)

V = [Vmin]
ps = [[0] for _ in range(Npumps)]  # which pump is active
last_active_pump = 0  # last active pump was the first one
pump_active = False  # No pump is working
for i in range(Nt - 1):
    t = i * deltaT
    if V[-1] >= Vmax and not pump_active:
        last_active_pump += 1
        last_active_pump %= Npumps
    Qout = 0
    for j in range(Npumps):
        if j == last_active_pump:
            if ps[j][-1] == 1:  # Pump j is active
                u = 1 if V[-1] >= Vmin else 0
            else:
                u = 1 if V[-1] >= Vmax else 0
        else:
            u = 0
        Qout += q[j] * u
        ps[j].append(u)
    pump_active = True if Qout > 0 else False
    V.append(V[-1] + deltaT * (Qin(t) - Qout))

# %% Plot
fig, ax1 = plt.subplots()
t = np.linspace(0, T, Nt)

color = "tab:red"
ax1.set_xlabel("Time [s]")
ax1.set_ylabel("Pump active", color=color)
ax1.plot(t, ps[0], color=color)
ax1.plot(t, ps[1], color=color, linestyle="dotted")
ax1.plot(t, ps[2], color=color, linestyle="dashed")
ax1.tick_params(axis="y", labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second Axes that shares the same x-axis

color = "tab:blue"
ax2.set_ylabel("Volume [m^3]", color=color)  # we already handled the x-label with ax1
ax2.plot(t, V, color=color)
ax2.tick_params(axis="y", labelcolor=color)

plt.grid()

# %%
