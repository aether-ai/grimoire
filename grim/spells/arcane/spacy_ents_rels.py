import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import sys, argparse, logging
import json
import os.path
from os import path

import spacy
import scispacy
from spacy import displacy
from spacy.matcher import Matcher 
from spacy.tokens import Span 

import graphviz as graphviz


HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem; margin-bottom: 2.5rem">{}</div>"""


@st.cache(allow_output_mutation=True)
def load_model(name):
    return spacy.load(name)


@st.cache(allow_output_mutation=True)
def process_text(model_name, text):
    nlp = load_model(model_name)
    return nlp(text)


def write_to_file(filename, content):
    f = open(filename, "a")
    f.write(content)
    f.close()


def get_relation(sent,nlp):

  doc = nlp(sent)

  # Matcher class object 
  matcher = Matcher(nlp.vocab)

  #define the pattern 
  pattern = [{'DEP':'ROOT'}, 
            {'DEP':'prep','OP':"?"},
            {'DEP':'agent','OP':"?"},  
            {'POS':'ADJ','OP':"?"}] 

  matcher.add("matching_1", None, pattern) 

  matches = matcher(doc)
  k = len(matches) - 1

  span = doc[matches[k][1]:matches[k][2]] 

  return(span.text)

def get_entities(sent,nlp):
  ## chunk 1
  ent1 = ""
  ent2 = ""

  prv_tok_dep = ""    # dependency tag of previous token in the sentence
  prv_tok_text = ""   # previous token in the sentence

  prefix = ""
  modifier = ""

  #############################################################
  
  for tok in nlp(sent):
    ## chunk 2
    # if token is a punctuation mark then move on to the next token
    if tok.dep_ != "punct":
      # check: token is a compound word or not
      if tok.dep_ == "compound":
        prefix = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          prefix = prv_tok_text + " "+ tok.text
      
      # check: token is a modifier or not
      if tok.dep_.endswith("mod") == True:
        modifier = tok.text
        # if the previous word was also a 'compound' then add the current word to it
        if prv_tok_dep == "compound":
          modifier = prv_tok_text + " "+ tok.text
      
      ## chunk 3
      if tok.dep_.find("subj") == True:
        ent1 = modifier +" "+ prefix + " "+ tok.text
        prefix = ""
        modifier = ""
        prv_tok_dep = ""
        prv_tok_text = ""      

      ## chunk 4
      if tok.dep_.find("obj") == True:
        ent2 = modifier +" "+ prefix +" "+ tok.text
        
      ## chunk 5  
      # update variables
      prv_tok_dep = tok.dep_
      prv_tok_text = tok.text
  #############################################################

  return [ent1.strip(), ent2.strip()]


def make_ent_rel_graph(row,graph):
    graph.edge(row["source"], row["target"], label=row["edge"])



def spell(spell_inputs):
    mana = spell_inputs
    st.write("Training text model")

    SPACY_MODEL_NAMES = ["en_core_web_sm", "en_core_web_md", "en_core_sci_sm"]

    spacy_model = st.selectbox("Model name", SPACY_MODEL_NAMES)
    model_load_state = st.info(f"Loading model '{spacy_model}'...")
    nlp = load_model(spacy_model)
    # nlp = spacy.load("en_core_web_sm")
    model_load_state.empty()

    try:
        doc = nlp(mana)
    except:
        st.error("Mana input is not sutiable for spacy model, using sample text")
        mana = "The tiger jumped over the table"
        st.write(mana)
        doc = nlp(mana)

    ents = []
    rels = []

    for sent in doc.sents:
        ent = get_entities(sent.text,nlp)
        rel = get_relation(sent.text,nlp)
        ents.append(ent)
        rels.append(rel)
        html = displacy.render(sent)
        html = html.replace("\n\n", "\n")
        st.write(HTML_WRAPPER.format(html), unsafe_allow_html=True)

    # extract subject
    source = [i[0] for i in ents]

    # extract object
    target = [i[1] for i in ents]

    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':rels})
    st.dataframe(kg_df)


    #ent_rels = parse_doc(doc,nlp)
    #t.write(ent_rels)
    

    graph = graphviz.Digraph()
    kg_df.apply(lambda row: make_ent_rel_graph(row,graph), axis=1)
    st.graphviz_chart(graph)

    # print ents and rels...

    return None, mana
