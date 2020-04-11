import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json


def spell(spell_inputs):
    mana = spell_inputs

    x_col = st.selectbox("Select x axis for Scatter plot", mana.columns)
    xcol_string = x_col + ":O"
    if st.checkbox("Show as continuous?", key="scatter_plot_x_is_cont"):
        xcol_string = x_col + ":Q"
    y_col = st.selectbox("Select y axis for Scatter plot", mana.columns)
    z_col = st.selectbox("Select z axis for Scatter plot", mana.columns)

    if st.checkbox("Show chart?", key="scatter_plot_show"):
        chart = (
            alt.Chart(mana)
            .mark_circle(size=60)
            .encode(x=xcol_string, y=y_col, color=z_col, tooltip=list(mana.columns))
            .interactive()
            .properties(title="Scatter Plot for " + x_col + "," + y_col + "," + z_col)
            .configure_title(fontSize=20,)
        )

        st.altair_chart(chart, use_container_width=True)
    return None, mana

