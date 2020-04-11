import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import matplotlib.pyplot as plt
import seaborn as sns

def spell(spell_inputs):
    mana = spell_inputs

    color = st.selectbox("Select column to pair", mana.columns)
    # target = st.selectbox("Select target for pair", mana.columns)
    # mana[color] = pd.Series(mana).map(dict(zip(range(len(mana.columns)-1),mana.columns)))
    if st.checkbox("Show chart?", key="pair_plot_show"):
        try:
            sns.pairplot(mana, hue=color)
        except:
            sns.pairplot(mana)
            st.error(color+" is not a valid column to pair")
            st.write("Showing base plot")
        st.pyplot()

    return None,mana

