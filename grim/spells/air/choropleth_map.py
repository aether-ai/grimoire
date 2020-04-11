import pandas as pd
import numpy as np
import streamlit as st
import sys, argparse, logging
import json
import plotly.express as px



def spell(spell_inputs):
    mana = spell_inputs


    if st.checkbox("Use test data?"):
        mana = px.data.gapminder()






    color_col = st.selectbox("Select color column for map", mana.columns)
    
    location_info = st.selectbox("Select location column for map", mana.columns)
    st.warning("Location column should be three letter country code i.e USA,BRA,NGA")

    if st.checkbox("Animate Map?"):
        time_col = st.selectbox("Select time column for map", mana.columns)
        fig = px.choropleth(mana, locations=location_info, color=color_col, animation_frame=time_col, range_color=[mana[color_col].min(), mana[color_col].max()])
    else:
        fig = px.choropleth(mana, locations=location_info, color=color_col, range_color=[mana[color_col].min(), mana[color_col].max()])

    



    



    st.plotly_chart(fig, use_container_width=True)
    return None, mana

    # df = pd.DataFrame(
    #     np.random.randn(1000, 2) / [50, 50] + [38.90, -77.03], columns=["lat", "lon"]
    # )


