import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.animation import FFMpegWriter


#Ecuaciones: 
# dT/dt = -k(Ti - Tj)
# dQ/dt = -K dT/dx

#Modelo: varios objetos cada uno con su respectiva k y T

#Número de cubos
N = 10

#Condiciones iniciales
Tamb = 298.15 #K
Tnp0 = 323.15 #k
k_agua = 1

#Inicializar T y k
T = np.ones(N)*Tamb
k = np.ones(N)*k_agua
dT_dt = np.ones(N)

#Cambiar T de la primera celda
T[0] = Tnp0#K
k[0] = 1

#Inicialización del tiempo
ti = 0
tf = 90
time_space = 10000
t = np.linspace(ti, tf, time_space)

dt = (tf - ti)/time_space

#Tiempo recalentamiento (cada T segundos se calienta a T[0])
dtheat = 30
Theat = dtheat #s
Theatplot = []
n = 1

#T de partícula
Tnp = [] 


#Inicio método numérico
for j in t:
    
    if j >= Theat:
        T[0] = Tnp0
        Theatplot.append(j)
        Theat = Theat + dtheat

    for i in range(N):
        # Límite izquierdo
        dT_dt[0] = -k[0] * (T[0] - T[1])

        # Cubos interiores
        for i in range(1, N-1):
            dT_dt[i] = k[i-1] * (T[i-1] - T[i]) - k[i] * (T[i] - T[i+1])

        # Límite derecho
        dT_dt[N-1] = k[N-2] * (T[N-2] - T[N-1])
        
    
    T_nueva = T.copy()
    
    for i in range(N):
        T_nueva[i] = T[i] + dT_dt[i]*dt
    
    T = T_nueva
    Tnp.append(T)
Tnp =np.array(Tnp)

for i in range(N):
    plt.plot(t, Tnp[:,i], label=f'Cubo {i}')
plt.title('Temperatura-Tiempo cubos')
plt.xlabel('Tiempo')
plt.ylabel('Temperatura')
plt.grid(True)
plt.legend()
for i in Theatplot:
    plt.axvline(i, color='gray', linestyle='--', alpha=0.4)
    plt.plot(i, Tnp0, 'ro') 
    plt.annotate(f'({i} s, {Tnp0} K)', xy=(i, Tnp0))

#plt.show()



fig, ax = plt.subplots()

# Initial heatmap (first time step)
heatmap = ax.imshow(
    Tnp[0].reshape(1, -1),
    aspect="auto",
    cmap="inferno",
    vmin=Tnp.min(),
    vmax=Tnp.max()
)

ax.set_xlabel("Cube index")
ax.set_ylabel("Temperature slice")
ax.set_title("Heat diffusion")

cbar = plt.colorbar(heatmap)
cbar.set_label("Temperature (K)")

def update(frame):
    heatmap.set_data(Tnp[frame].reshape(1, -1))
    ax.set_title(f"Heat diffusion — t = {frame*dt:.2f} s")
    return [heatmap]

ani = FuncAnimation(
    fig,
    update,
    frames=range(0, len(Tnp),5),
    interval=1
)

    
plt.show()
