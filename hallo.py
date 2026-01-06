import plotly.graph_objects as go
import numpy as np
import streamlit as st

t = st.slider("Tiempo", 0.0, 10.0, 0.0, 0.1)

fig = go.Figure(
    data=go.Scatter(x=[t], y=[np.sin(t)], mode="markers"),
    layout=go.Layout(
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[-1, 1])
    )
)

st.plotly_chart(fig)

