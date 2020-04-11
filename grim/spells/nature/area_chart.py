import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json


def spell(spell_inputs):
    mana = spell_inputs

    x_col = st.selectbox("Select x axis for area chart", mana.columns)
    xcol_string = x_col + ":O"
    if st.checkbox("Show as continuous?", key="area_chart_x_is_cont"):
        xcol_string = x_col + ":Q"
    y_col = st.selectbox("Select y axis for area chart", mana.columns)
    z_col = st.selectbox("Select z axis for area chart", mana.columns)

    if st.checkbox("Show chart?", key="area_chart_show"):
        chart = (
            alt.Chart(mana)
            .mark_area()
            .encode(
                x=xcol_string,
                y="sum(" + y_col + ")",
                color=z_col,
                tooltip=list(mana.columns),
            )
            .interactive()
            .properties(title="Area Chart for " + x_col + "," + y_col + "," + z_col)
            .configure_title(fontSize=20,)
            .configure_axis(labelFontSize=20, titleFontSize=20)
            .configure_legend(labelFontSize=20, titleFontSize=20)
        )

        st.altair_chart(chart, use_container_width=True)
    return None, mana
