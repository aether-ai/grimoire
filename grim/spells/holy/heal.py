import streamlit as st
import sys, argparse, logging
import json
import random
import time
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split


def spell(spell_inputs):
    mana = spell_inputs
    # st.dataframe(mana)
    target_string = st.selectbox("Select target for model", mana.columns)

    target = np.array(mana[target_string])
    dropcol = [target_string]
    for column in mana:
        if "Unnamed" in column:
            dropcol.append(column)
            continue
        try:
            float(mana[column][1])
        except:
            logging.debug("Drop this col as not a float: " + column)
            dropcol.append(column)

    try:
        logging.debug("dropping features with axis")
        features = mana.drop(dropcol, axis=1)
    except:
        logging.debug("dropping features with NO axis")
        features = mana.drop(dropcol, axis=0)

    # save list of strings of features
    feature_list = list(features.columns)

    # convert features to numpy
    featuresarr = np.array(features)
    randInt = random.randint(1, 200)

    test_features, train_features, test_target, train_target, = train_test_split(
        featuresarr, target, test_size=0.75, random_state=randInt
    )  # what data to split and how to do it.

    healed_data = {}
    healed_data["train_features"] = train_features.tolist()
    healed_data["train_target"] = train_target.tolist()
    healed_data["test_features"] = test_features.tolist()
    healed_data["test_target"] = test_target.tolist()
    healed_data["feature_list"] = feature_list
    healed_data["features_arr"] = featuresarr.tolist()
    healed_data["target"] = target.tolist()
    healed_data["target_string"] = target_string
    healed_data["mana"] = mana
    healed_data["mana_len"] = len(mana)

    if st.checkbox("Show Healed data"):
        st.write(healed_data)
    return healed_data, mana

