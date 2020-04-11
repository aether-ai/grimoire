import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
#import umap
import umap.umap_ as umap


def spell(spell_inputs):
    mana = spell_inputs

    target_string = st.selectbox("Select target for UMAP", mana.columns)
    dropcol = []
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
        features = mana.drop(dropcol, axis=1).dropna()
    except:
        logging.debug("dropping features with NO axis")
        features = mana.drop(dropcol, axis=0).dropna()

    reducer = umap.UMAP()
    embedding = reducer.fit_transform(features)
    embedding.shape

    embedding_df = pd.DataFrame(embedding, columns=("x", "y"))

    for column in mana.columns:
        embedding_df[column] = mana[column]

    chart = (
        alt.Chart(embedding_df)
        .mark_circle(size=100)
        .encode(x="x", y="y", color=target_string, tooltip=list(embedding_df.columns))
        .interactive()
        .properties(title="UMAP Embedding")
        .configure_title(fontSize=20,)
        .configure_axis(labelFontSize=20, titleFontSize=20)
        .configure_legend(labelFontSize=20, titleFontSize=20)
    )

    st.altair_chart(chart, use_container_width=True)
    return None,mana


    #do an inverse transform #todo not working
    # test_pts = np.array([0,1])
    # inv_transformed_points = mapper.inverse_transform(test_pts)
    # st.write(inv_transformed_points)

