###### Grimoire Streamlit Runner ######
import streamlit as st
import numpy as np
import pandas as pd
import time
import json
import sys, argparse, logging
from spells import REGISTERED_SPELLS
from io import StringIO
from PIL import Image
import requests
from io import BytesIO
import os

@st.cache(allow_output_mutation=True)
def load_image(data):
    return Image.open(data)


@st.cache(allow_output_mutation=True)
def load_mana(mana_type, data):

    if mana_type == "csv":
        mana = pd.read_csv(data)
    elif mana_type == "json":
        mana = pd.read_json(data)
    return mana


def set_mana(mana_choice):

    if mana_choice == "CSV":
        st.write("### Select how you will load the CSV")
        csv_choices = ["Upload", "URL", "Free text"]
        csv_choice = st.selectbox("Select csv loading type", csv_choices)
        if csv_choice == "Upload":
            data = st.file_uploader("Choose a CSV file", type="csv")
        if csv_choice == "URL":
            data = st.text_input("URL:", "")
        if csv_choice == "Free text":
            raw_data = st.text_area("Enter Data", "")
            data = None
            if raw_data is not "":
                data = StringIO(raw_data)

        if data is not None:
            if data is not "":
                mana = load_mana("csv", data)
                return mana

    elif mana_choice == "JSON":
        st.write("### Select how you will load the JSON")
        json_choices = ["Upload", "URL", "Free text"]
        json_choice = st.selectbox("Select json loading type", json_choices)
        if json_choice == "Upload":
            data = st.file_uploader("Choose a JSON file", type="json")
        if json_choice == "URL":
            data = st.text_input("URL:", "")
        if json_choice == "Free text":
            raw_data = st.text_area("Enter Data")
            data = None
            if raw_data is not "":
                data = StringIO(raw_data)

        if data is not None:
            if data is not "":
                mana = load_mana("json", data)
                return mana
    elif mana_choice == "Image":
        st.write("### Select how you will load the Image")
        image_choices = ["Upload", "URL"]
        image_choice = st.selectbox("Select json loading type", image_choices)
        if image_choice == "Upload":
            data = st.file_uploader("Choose an Image file", type="png,jpg")
        if image_choice == "URL":
            url = st.text_input("URL:", "")
            data = None
            if url is not "":
                response = requests.get(url)
                data = BytesIO(response.content)
        if data is not None:
            if data is not "":
                mana = load_image(data)
                st.image(mana, use_column_width=True)
                return mana
    elif mana_choice == "Free text":
        st.write("Free text")
        mana = st.text_area("Enter Data")
        return mana
    elif mana_choice == "Database":
        st.write("Database")
        st.error("todo")
    elif mana_choice == "Data Files":
        return "Data Files"
    elif mana_choice == "None":
        return "None"
    else:
        st.balloons()
        st.error("Congrats you broke the system")

    return


def main():
    grim = []
    grim_path = "grim_st.json"
    try:
        with open(grim_path) as json_file:
            grim = json.load(json_file)
    except:
        st.error("No grim_st.json file")
        return

    #print(grim["name"])
    st.title("Grimoire: " + grim["name"])
    st.markdown("## " + grim["value"])
    spell_tomb = {}

    if "isTest" in grim and grim["isTest"]:
        hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
        st.markdown(hide_streamlit_style, unsafe_allow_html=True)
        st.markdown("### Using Sample Data")
        data = "sample_data/iris.csv"
        mana = pd.read_csv(data)
        #st.write(mana)
    else:
        mana_choices = [
            "CSV",
            "JSON",
            "Free text",
            "Image",
            "Database",
            "Data Files",
            "None",
        ]

        mana_choice = st.selectbox("Select data format", mana_choices)
        try:
            mana = set_mana(mana_choice)
        except Exception as e:
            show_error = st.checkbox("Show Error details?")

            if show_error:
                st.write(e)
            st.error("Invalid input")
            return

        # st.markdown('### Before you can cast your spells, upload your data')
        # data = st.file_uploader("Choose a CSV file", type="csv")
    spell_count = 1

    st.sidebar.title("Grimoire: " + grim["name"])
    image = Image.open("assets/spellbook.png")
    st.sidebar.image(image, use_column_width=True, format="png")
    if mana is not None:

        st.write(mana)

        # mana = pd.read_csv(data)
        if st.sidebar.checkbox(
            "Add markdown at start?", key="add_markdown-start-" + str(spell_count)
        ):
            markdown_text = st.sidebar.text_area(
                "Enter Markdown Text", key="markdown-start-text-" + str(spell_count)
            )
            st.markdown(markdown_text)

        for spell in grim["spells"]:
            spell_name = spell["spell_name"]
            spell_type = spell["spell_type"]
            spell_info = spell["spell_info"]
            spell_inputs = spell["spell_inputs"]
            spell_output = spell["spell_output"]
            takes_mana = spell["takes_mana"]
            for spell_input in spell_inputs.keys():
                # only add input if not in tomb
                if spell_input not in spell_tomb:
                    spell_tomb[spell_input] = spell_inputs[spell_input]
                else:
                    # spell input is in tomb, replace value
                    spell_inputs[spell_input] = spell_tomb[spell_input]

            st.markdown("## Casting spell: " + spell_type + " " + spell_name)
            st.markdown("### " + spell_info)

            # first spell must take mana as input
            try:
                if takes_mana:
                    # would have to do a check here? or pass in mana
                    spell_tomb[spell_output], mana = REGISTERED_SPELLS[spell_name](mana)
                else:
                    spell_tomb[spell_output], mana = REGISTERED_SPELLS[spell_name](
                        spell_inputs
                    )

                if st.sidebar.checkbox(
                    "Add markdown after spell " + spell_name + "?",
                    key="add_markdown-end-" + str(spell_count),
                ):
                    markdown_text = st.sidebar.text_area(
                        "Enter Markdown Text",
                        key="markdown-end-text-" + str(spell_count),
                    )
                    st.markdown(markdown_text)
            except Exception as e:
                show_error = st.checkbox("Show Error details?", key="spell_cast_errors")
                if show_error:
                    st.write(e)
                st.error("Invalid input")
                return
            spell_count += 1


if __name__ == "__main__":
    main()
