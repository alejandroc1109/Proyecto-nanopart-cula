import streamlit as st
import pandas as pd


df = pd.DataFrame({
    "t (s)": [0, 1, 2, 3],
    "T (K)": [300, 295, 291, 288]
})

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True
)


