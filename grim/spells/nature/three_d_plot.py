import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import time
import plotly.graph_objects as go


def spell(spell_inputs):

    mana = spell_inputs
    # time_col = st.selectbox("Select time axis for bar chart", mana.columns)
    # size_col = st.selectbox("Select size axis for bar chart", mana.columns)
    x_col = st.selectbox("Select x axis for bar chart", mana.columns)
    xcol_string = x_col
    if st.checkbox("Show as continuous?", key="bar_chart_x_is_cont"):
        xcol_string = x_col
    y_col = st.selectbox("Select y axis for bar chart", mana.columns)
    z_col = st.selectbox("Select z axis for bar chart", mana.columns)


    if st.checkbox("Show chart?", key="three_d_plot_show"):
        fig = go.Figure(
            data=[
                go.Mesh3d(
                    x=(mana[x_col]),
                    y=(mana[y_col]),
                    z=(mana[z_col]),
                    opacity=0.5,
                    color="rgba(244,22,100,0.6)",
                )
            ]
        )

        fig.update_layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[mana[x_col].min(), mana[x_col].max()],),
                yaxis=dict(nticks=4, range=[mana[y_col].min(), mana[y_col].max()],),
                zaxis=dict(nticks=4, range=[mana[z_col].min(), mana[z_col].max()],),
            ),
            width=700,
            margin=dict(r=20, l=10, b=10, t=10),
        )

        # fig.show()
        st.plotly_chart(fig, use_container_width=True)

    return None, mana
