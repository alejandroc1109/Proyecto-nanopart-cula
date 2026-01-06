import numpy as np
import matplotlib.pyplot as plt
import streamlit as st 
import time




#Ecuaciones: 
# dT/dt = -k(Ti - Tj)
# dQ/dt = -K dT/dx

#Modelo: varios objetos cada uno con su respectiva k y T
st.title("Simulation heat transfer between cubes 🥵")

#Número de cubos
N = st.slider('Cubes number', 2, 10)

#Condiciones iniciales
Tamb = 298.15 #K
Tnp0 = st.number_input("Nanoparticle temperature [K]", value=Tamb, format="%.2f") #k
k_agua = 1

#Inicializar T y k
T = np.ones(N)*Tamb
k = np.ones(N)*k_agua
dT_dt = np.ones(N)

#Cambiar T de la primera celda
T[0] = Tnp0


k[0] = st.number_input("Nanoparticle cooling constant [1/s]", value=1.0, format="%.2f")

#Inicialización del tiempo
ti = 0
tf = st.number_input("Stop simulation after [s]:", value=60.0, format="%.1f")
time_space = 10000
t = np.linspace(ti, (tf+tf/time_space), time_space)
dt = (tf - ti)/time_space

#Tiempo recalentamiento (cada T segundos se calienta a T[0])
dtheat = st.number_input('Heating time [s]:', value=100000.0, format='%.1f')
Theat = dtheat #s
Theatplot = []
n = 1


#Condiciones simulación
st.write("Nanoparticule temperature [K]", T[0])
st.write("Nanoparticle cooling constant [1/s]", k[0])
st.write("Simulation will be stopped after [s]", tf)
st.write("Heating time [s]", dtheat)
st.write("Water temperature [K]", Tamb)


if st.button("Click here to start the simulation"):
    st.write('Simulation started')
    if st.button('Finish simulation'):
        st.session_state.stop = True
    
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

    col1, col2 = st.columns(2)
    
    with col1:
        # Crear figura y ejes
        grafica, ax = plt.subplots()

        # Gráficas principales
        for i in range(N):
            ax.plot(t, Tnp[:, i], label=f'Cube {i+1}')

        # Etiquetas y formato
        ax.set_title('Temperature vs Time')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Temperature [K]')
        ax.grid(True)
        ax.legend()

        # Líneas verticales y anotaciones
        for i in Theatplot:
            ax.axvline(i, color='gray', linestyle='--', alpha=0.4)
            ax.plot(i, Tnp0, 'ro')
            ax.annotate(f'({i:.1f} s, {Tnp0:.1f} K)', xy=(i, Tnp0))

        st.pyplot(grafica)

    with col2:
        fig, ax = plt.subplots()
        heatmap = ax.imshow(
            Tnp[0].reshape(1, -1),
            aspect="auto",
            cmap="inferno",
            extent=[0, N, 0, 1],
            vmin=Tnp.min(),
            vmax=Tnp.max()
        )

        ax.set_xlabel("Cube")
        ax.set_ylabel("Temperature")
        ax.set_xticks(np.arange(1, N+1, 1))
        ax.set_yticks([])
        cbar = plt.colorbar(heatmap, ax=ax)

        plot_area = st.empty()

        frames = list(range(0, time_space, 50))
        frames.append(9999)
        time.sleep(1.5)
        for frame in frames:
            heatmap.set_data(Tnp[frame].reshape(1, -1))
            ax.set_title(f"Heat diffusion vs time = {frame*dt:.1f} s")
            plot_area.pyplot(fig)
            time.sleep(0.01)