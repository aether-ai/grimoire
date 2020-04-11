import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json


def highlight_greaterthan(s, threshold, column, mana_clone):
    is_max = pd.Series(data=False, index=s.index)
    is_max[column] = s.loc[column] >= threshold
    return ["background-color: yellow" if is_max.any() else "" for v in is_max]


def highlight_lessthan(s, threshold, column, mana_clone):
    is_min = pd.Series(data=False, index=s.index)
    is_min[column] = s.loc[column] <= threshold
    return ["background-color: yellow" if is_min.any() else "" for v in is_min]


def highlight_equals(s, threshold, column, mana_clone):
    is_min = pd.Series(data=False, index=s.index)
    is_min[column] = s.loc[column] == threshold
    return ["background-color: yellow" if is_min.any() else "" for v in is_min]


def highlight_contains(s, threshold, column, mana_clone):
    is_min = pd.Series(data=False, index=s.index)
    # is_min[column] = threshold in s.loc[column]
    for col in s.loc[column]:
        if threshold in str(col):
            is_min[column] = s.loc[column]
            # mana_clone = is_min
            # print(s)
    return ["background-color: yellow" if is_min.any() else "" for v in is_min]


def spell(spell_inputs):
    mana = spell_inputs

    highlight_choices = [
        "Max",
        "Min",
        "Null",
        "Equals",
        "Less Than",
        "Greater Than",
        "Heatmap",
        "Contains",
    ]

    highlight_choice = st.selectbox("Select highlight option", highlight_choices)

    mana_clone = pd.DataFrame(index=mana.index, columns=mana.columns)

    if highlight_choice == "Max":
        st.dataframe(mana.style.highlight_max(axis=0))
    if highlight_choice == "Min":
        st.dataframe(mana.style.highlight_min(axis=0))
    if highlight_choice == "Null":
        try:
            st.dataframe(mana.style.highlight_null(axis=0))
        except:
            st.success("No NULL values")
            st.write(mana)
    if highlight_choice == "Heatmap":
        st.dataframe(mana.style.background_gradient(axis=0))
    if highlight_choice == "Greater Than":

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            threshold = st.number_input("Value: ", 1.0)
            st.dataframe(
                mana.style.apply(
                    highlight_greaterthan,
                    threshold=threshold,
                    column=what_cols,
                    axis=1,
                    mana_clone=mana_clone,
                )
            )
    if highlight_choice == "Less Than":

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            threshold = st.number_input("Value: ", 1.0)
            st.dataframe(
                mana.style.apply(
                    highlight_lessthan,
                    threshold=threshold,
                    column=what_cols,
                    axis=1,
                    mana_clone=mana_clone,
                )
            )
    if highlight_choice == "Equals":
        equal_choices = ["Number", "Text"]
        equal_choice = st.selectbox("Select equals option", equal_choices)

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            if equal_choice == "Number":
                threshold = st.number_input("Value: ", 1.0)
            if equal_choice == "Text":
                threshold = st.text_input("Value: ", "")
            st.dataframe(
                mana.style.apply(
                    highlight_equals,
                    threshold=threshold,
                    column=what_cols,
                    axis=1,
                    mana_clone=mana_clone,
                )
            )

    if highlight_choice == "Contains":

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            threshold = st.text_input("Value: ", "")
            st.dataframe(
                mana.style.apply(
                    highlight_contains,
                    threshold=threshold,
                    column=what_cols,
                    axis=1,
                    mana_clone=mana_clone,
                )
            )
    return None, mana
