import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json


def search_filter(row, cols, value):
    #df.apply returns the rows or columns as list
    contained = False
    for col in cols:
        #string is a number here, so we must cast it.
        if value in str(row[col]):
            contained = True
            return True

    return contained


def spell(spell_inputs):
    mana = spell_inputs
    mana_clone = None

    filter_choices = [
        "First N Rows",
        "Equals",
        "Remove Null",
        "Less Than",
        "Greater Than",
        "Contains",
    ]

    filter_choice = st.selectbox("Select filter option", filter_choices)

    if filter_choice == "First N Rows":
        threshold = st.number_input("Value: ", 10)
        mana_clone = mana.head(threshold)

    if filter_choice == "Remove Null":
        mana_clone = mana.dropna()

    if filter_choice == "Greater Than":

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            threshold = st.number_input("Value: ", 1.0)
            df_query = ""
            cond_count = 1
            for cond in what_cols:
                df_query += "`"+cond + "` >= " + str(threshold)

                if cond_count == len(what_cols):
                    pass
                else:
                    df_query += " or "
                cond_count += 1

            st.write("Query: "+df_query)
            mana_clone = mana.query(df_query)
    if filter_choice == "Less Than":

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            threshold = st.number_input("Value: ", 1.0)
            df_query = ""
            cond_count = 1
            for cond in what_cols:
                df_query += "`"+cond + "` <= " + str(threshold)

                if cond_count == len(what_cols):
                    pass
                else:
                    df_query += " or "
                cond_count += 1

            st.write("Query: "+df_query)
            mana_clone = mana.query(df_query)

    if filter_choice == "Equals":
        equal_choices = ["Number", "Text"]
        equal_choice = st.selectbox("Select equals option", equal_choices)

        what_cols = st.multiselect("Columns", mana.columns)
        comp_vals = []

        if len(what_cols) > 0:
            if equal_choice == "Number":
                threshold = st.number_input("Value: ", 1.0)
                comp_vals.append(threshold)
            if equal_choice == "Text":
                threshold = st.text_input("Value: ", "")
                comp_vals.append(threshold)

            df_query = ""
            cond_count = 1
            for cond in what_cols:

                if equal_choice == "Text":
                    df_query += "`"+cond + "` == '" + threshold + "'"
                elif equal_choice == "Number":
                    df_query += "`"+cond + "` == " + str(threshold)

                if cond_count == len(what_cols):
                    pass
                else:
                    df_query += " or "
                cond_count += 1

            st.write("Query: "+df_query)
            mana_clone = mana.query(df_query)
            # mana_clone = mana.loc[mana[what_cols].isin(comp_vals)]

    if filter_choice == "Contains":

        what_cols = st.multiselect("Columns", mana.columns)

        if len(what_cols) > 0:
            threshold = st.text_input("Value: ", "")

            if threshold is not "":
                search_results = mana.apply(lambda row: search_filter(row,what_cols,threshold), axis=1)
                mana_clone = mana[search_results]

    if mana_clone is not None:
        st.dataframe(mana_clone)

        if st.checkbox("Set selected as current data?"):
            mana = mana_clone
    return None, mana
