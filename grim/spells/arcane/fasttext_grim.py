import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import fasttext
import os.path
from os import path


def reset_file(filename):
    f = open(filename, "w")
    f.write("")
    f.close()


def write_to_file(filename, content):
    f = open(filename, "a")
    f.write(content)
    f.close()


def make_text_file_from_df(filename, row):

    labels = str(row["label"]).split(";")
    label_text = ""
    for label in labels:
        label_text += "__label__" + str(label) + " "

    text = label_text + str(row["text"])

    write_to_file(filename, str(text) + "\n")


def does_model_exsit(model_string):
    if path.exists(model_string):
        print("model exists")
        return True
    else:
        print("model does not exist")
        return False


def load_model(model_output_loc):
    model = fasttext.load_model(model_output_loc)
    return model


def train_model(train_filename, test_filename):
    # can play with settings latter
    model = fasttext.train_supervised(input=train_filename)

    # save model output
    model_output_loc = "models/fasttext/model.bin"
    model.save_model(model_output_loc)
    print("saving model to: " + model_output_loc)

    # train model
    metrics = model.test(test_filename)
    # st.write("Tested: "+str(metrics[0]))
    # st.write("Precision: "+str(metrics[1]))
    # st.write("Recall: "+str(metrics[2]))

    metrics_json = {}
    metrics_json["tested"] = str(metrics[0])
    metrics_json["precision"] = str(metrics[1])
    metrics_json["recall"] = str(metrics[2])

    json_path = "models/fasttext/model.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(metrics_json, f, ensure_ascii=False, indent=4)

    return model, metrics_json


def spell(spell_inputs):
    mana = spell_inputs
    st.write("Training text model")

    label = st.selectbox("Select label column ", mana.columns)
    st.warning("Can have multiple labels by using ; between each one")
    text = st.selectbox("Select text column", mana.columns)

    # select label column
    # select text column
    text_df = mana[[label, text]].rename(columns={label: "label", text: "text"})

    st.write(text_df)

    model = None
    model_string = "models/fasttext/model.bin"
    if does_model_exsit(model_string):
        model = load_model(model_string)
        json_path = "models/fasttext/model.json"
        with open(json_path) as json_file:
            metrics_json = json.load(json_file)
    else:
        pass

    if st.button("Train Model"):
        # create text file, might change..
        filename = "models/fasttext/dataset.txt"
        reset_file(filename)
        text_df.apply(lambda row: make_text_file_from_df(filename, row), axis=1)

        # should make a train/test split
        msk = np.random.rand(len(text_df)) < 0.75
        train = text_df[msk]
        train_filename = "models/fasttext/dataset.train"
        reset_file(train_filename)
        train.apply(lambda row: make_text_file_from_df(train_filename, row), axis=1)

        test = text_df[~msk]
        test_filename = "models/fasttext/dataset.test"
        reset_file(test_filename)
        test.apply(lambda row: make_text_file_from_df(test_filename, row), axis=1)

        model_string = "models/fasttext/model.bin"
        json_string = "models/fasttext/model.json"
        reset_file(model_string)
        reset_file(json_string)

        model, metrics_json = train_model(train_filename, test_filename)

    if model is not None:

        st.write("Tested: " + str(metrics_json["tested"]))
        st.write("Precision: " + str(metrics_json["precision"]))
        st.write("Recall: " + str(metrics_json["recall"]))

        pred_text = st.text_input("Type text to predict")
        if pred_text is not None:
            preds = model.predict(pred_text, k=-1)
            counter = 0

            for result in preds[0]:
                st.success(
                    result.replace("__label__", "Label: ")
                    + ", probability: "
                    + str(preds[1][counter])
                )
                counter += 1
    return model,mana
