import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import os
import glob
from PIL import Image
from io import StringIO
import requests
from io import BytesIO


def does_model_exsit(target_string):
    # TODO: update save model with grim name
    model_output_loc = "/tmp/output_graph.pb"

    if path.exists(model_output_loc):
        print("model exists")
        return True
    else:
        print("model does not exist")
        return False


@st.cache(allow_output_mutation=True)
def get_images(label, image_files):
    image_urls = []
    for image_url in image_files:
        try:
            image = Image.open(image_url)
            image_urls.append(image_url)
        except:
            pass
    return image_urls


def spell(spell_inputs):
    mana = spell_inputs

    st.write("Image classifer")

    if isinstance(mana, pd.DataFrame):
        st.warning("CSV training soon...")
        return
        # st.write("Mana is dataframe")

        # # select image url
        # image_col = st.selectbox("Select image column", mana.columns)

        # # select label column
        # label_col = st.selectbox("Select label column", mana.columns)

        # if st.button("Train Model"):
        #     # download images to corresponding label folder
        #     st.write("todo")

        #     # train model

        #     # train_model(svm_model, healed_data, target_string)

    else:
        if mana == "Data Files":
            st.write("Data Files")
            st.write("Each label should be a folder in data_files/images")

            labels = os.listdir("data_files/images")
            label_choices = st.multiselect("Select labels", labels)

            for label in label_choices:
                st.markdown("## " + label)

                image_files = glob.glob("data_files/images/" + label + "/*")
                # display 50 images from choice
                image_urls = get_images(label, image_files)

                st.image(image_urls, width=50)

                # image = Image.open('sunrise.jpg')
                # st.image(image)

            if len(label_choices) >= 2:
                st.warning("This will take a while...")
                if st.button("Train Model"):
                    cmd = "python helpers/image_model/retrain.py --image_dir data_files/images"
                    with st.spinner("Model Training"):
                        os.system(cmd)
                        st.success("done")
                        st.balloons()

            if does_model_exsit:
                st.write("Predict Label")
                url = st.text_input("URL:", "")

                if url is not "":
                    response = requests.get(url)
                    data = BytesIO(response.content)

                    try:

                        image = Image.open(data)
                        st.image(image)

                        # save file to temp file
                        temp_loc = "/tmp/test_image"
                        with open(temp_loc, "wb") as out:
                            out.write(data.getbuffer())

                        cmd = "python helpers/image_model/label_image.py --graph=/tmp/output_graph.pb --labels=/tmp/output_labels.txt --input_layer=Placeholder --output_layer=final_result --image=/tmp/test_image"
                        with st.spinner("Predicting..."):
                            pred_string = os.popen(cmd).read()
                            pred_array = pred_string.split("\n")

                        for pred in pred_array:
                            st.markdown("# " + pred)
                    except Exception as e:
                        st.error("URL is not image")
                        st.write(e)
        else:
            st.error("Data Files only supported")

    return None, mana
