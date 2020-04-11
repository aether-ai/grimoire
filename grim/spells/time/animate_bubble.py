import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import time
import plotly.express as px



def spell(spell_inputs):

    mana = spell_inputs
    time_col = st.selectbox("Select time column", mana.columns)
    color_col = st.selectbox("Select color column", mana.columns)
    size_col = st.selectbox("Select size column", mana.columns)

    x_col = st.selectbox("Select x axis for bar chart", mana.columns)
    y_col = st.selectbox("Select y axis for bar chart", mana.columns)
    z_col = st.selectbox("Select z axis for bar chart", mana.columns)

    fig = px.scatter(
        mana,
        x=x_col,
        y=y_col,
        animation_frame=time_col,
        animation_group=z_col,
        size=size_col,
        color=color_col,
        log_x=True,
        size_max=45,
        range_x=[mana[x_col].min(), mana[x_col].max()],
        range_y=[mana[y_col].min(), mana[y_col].max()],
    )
    st.plotly_chart(fig, use_container_width=True)
    return None, mana

