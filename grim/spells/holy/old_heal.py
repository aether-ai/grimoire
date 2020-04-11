import sys, argparse, logging
import json
import random
import time
import pandas as pd, numpy as np
from sklearn.model_selection import train_test_split



#get data
def mana_extract(mana_location):
    try:
        print(mana_location)
        mana = pd.read_csv(mana_location)
        return mana
    except Exception as e:
        logging.info("Yikes bad error")
        logging.error(e)
        sys.exit(-1)

#heal data
def spell(spell_inputs):
    logging.info("heal spell")
    mana_location = spell_inputs["mana_location"]
    target_string = spell_inputs["target_string"]
    mana = mana_extract(mana_location)

    logging.debug("Target data is :"+ target_string)
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

    train_features, test_features, train_target, test_target = train_test_split(
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
    healed_data["mana"] = mana.values.tolist()
    healed_data["mana_len"] = len(mana)

    return healed_data
    