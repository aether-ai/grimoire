import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import time


def spell(spell_inputs):


    mana = spell_inputs
    st.markdown("## Create the graph you would like to animate")
    time_col = st.selectbox("Select time column", mana.columns)
    curr_time = st.selectbox("Select time", mana[time_col].unique())

    x_col = st.selectbox("Select x axis for line chart", mana.columns)
    xcol_string=x_col+":O"
    if st.checkbox("Show as continuous?",key="time_line_x_is_cont"):
        xcol_string=x_col+":Q"     
    y_col = st.selectbox("Select y axis for line chart", mana.columns)
    ycol_string=alt.Y(y_col)
    if st.checkbox("Show as sorted?",key="time_line_sort_y"):
        ycol_string=alt.Y(y_col, sort="-x")   
    z_col = st.selectbox("Select z axis for line chart", mana.columns)

    time_mana = mana.loc[mana[time_col] == curr_time]

    chart = (
        alt.Chart(time_mana)
        .mark_line(point=True)
        .encode(
            y=ycol_string,
            x=xcol_string,
            color=z_col,
            tooltip=list(time_mana.columns),
        )
        .properties(
            title="Line graph of " + x_col + "," + y_col + " at " + str(curr_time)
        )
        .configure_title(fontSize=20,)
        .configure_axis(labelFontSize=20, titleFontSize=20)
        .configure_legend(labelFontSize=20, titleFontSize=20)
    ).properties(height=700)

    st.altair_chart(chart, use_container_width=True)

    # basicaly the animate button should make n graphs and show them and have a time.sleep in between

    st.markdown("## Animate the graph above using "+time_col+" as the time.")

    time_interval = st.number_input("Time interval", 0.0, None, value=1.0)

    if st.button("Animate Graph"):

        # declare an empty obj here then update it in loop
        time_chart = st.empty()
        sorted_vals = mana[time_col].unique()
        sorted_vals.sort()
        for times in sorted_vals:

            curr_time_mana = mana.loc[mana[time_col] <= times]
            st.write(times)
            curr_chart = (
                alt.Chart(curr_time_mana)
                .mark_line(point=True)
                .encode(
                    y=ycol_string,
                    x=xcol_string,
                    color=z_col,
                    tooltip=list(time_mana.columns),
                )
                .properties(
                    title="Line graph of " + x_col + "," + y_col + " at " + str(times)
                )
                .configure_title(fontSize=20,)
                .configure_axis(labelFontSize=20, titleFontSize=20)
                .configure_legend(labelFontSize=20, titleFontSize=20)
            ).properties(height=700)
            time_chart.altair_chart(curr_chart, use_container_width=True)
            # sleep
            time.sleep(time_interval)
    
    return None,mana
