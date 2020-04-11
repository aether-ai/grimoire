import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json


def spell(spell_inputs):
    mana = spell_inputs

    x_col = st.selectbox("Select x axis for heatmap", mana.columns)
    xcol_string=x_col+":O"
    if st.checkbox("Show as continuous?",key="heatmap_x_is_cont"):
        xcol_string=x_col+":Q"
    y_col = st.selectbox("Select y axis for heatmap", mana.columns)
    z_col = st.selectbox("Select z axis for heatmap", mana.columns)

    if st.checkbox("Show chart?", key="heatmap_show"):
        chart = (
            alt.Chart(mana)
            .mark_rect()
            .encode(x=xcol_string, y=y_col, color=z_col,tooltip=list(mana.columns))
            .properties(title="Heatmap for " + x_col + "," + y_col + "," + z_col)
            .configure_title(fontSize=20,)
            .configure_axis(labelFontSize=20, titleFontSize=20)
            .configure_legend(labelFontSize=20, titleFontSize=20)
        )
    
        # text = chart.mark_text(baseline="middle").encode(
        #     text=z_col, color=alt.value("black")
        # )
    
        st.altair_chart(chart, use_container_width=True)
    return None,mana

