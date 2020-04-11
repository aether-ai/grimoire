import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json


def spell(spell_inputs):
    mana = spell_inputs

    hist_col = st.selectbox("Select column for histogram", mana.columns)

    "You selected: ", hist_col

    chart = (
        alt.Chart(mana)
        .mark_bar()
        .encode(alt.X(hist_col, bin=True), y="count()")
        .properties(title="Histogram for " + hist_col)
        .configure_title(fontSize=20,)
        .configure_axis(labelFontSize=20, titleFontSize=20)
        .configure_legend(labelFontSize=20, titleFontSize=20)
    )

    st.altair_chart(chart, use_container_width=True)
    return None,mana
