import pandas as pd
import numpy as np
import streamlit as st
import sys, argparse, logging
import json


def spell(spell_inputs):
    mana = spell_inputs


    lat = st.selectbox("Select latitude column", mana.columns)
    lon = st.selectbox("Select longitude column", mana.columns)

    # df = pd.DataFrame(
    #     np.random.randn(1000, 2) / [50, 50] + [38.90, -77.03], columns=["lat", "lon"]
    # )
    try:
        st.map(mana[[lat,lon]].rename(columns={lat:"lat",lon:"lon"}))
    except Exception as e:
        show_error = st.checkbox("Show Error Details?")
        if show_error:
            st.write(e)
        st.error("Points are not latlong")
        st.success("Here is an example dataframe with correct values")
        df = pd.DataFrame(np.random.randn(10, 2) / [50, 50] + [38.90, -77.03], columns=["lat", "lon"])
        st.write(df)
        #st.map(df)
    return None,mana

