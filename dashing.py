import plotly.graph_objects as go
import numpy as np

t = np.linspace(0, 10, 100)
frames = []

# Generamos datos cambiantes
for k in range(50):
    y = np.sin(t + 0.1 * k)
    frames.append(
        go.Frame(
            data=[go.Scatter(x=t, y=y)],
            name=str(k)
        )
    )

fig = go.Figure(
    data=[go.Scatter(x=t, y=np.sin(t))],
    frames=frames
)

fig.update_layout(
    title="Animación de onda",
    xaxis_title="Tiempo",
    yaxis_title="Amplitud",
    updatemenus=[{
        "type": "buttons",
        "buttons": [{
            "label": "Play",
            "method": "animate",
            "args": [None]
        }]
    }]
)

fig.show()
