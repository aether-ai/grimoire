import pandas as pd, numpy as np
import sys, argparse, logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor  # get the model
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV
import sklearn.metrics
import pickle
import random
import streamlit as st
import altair as alt
import os.path
from os import path
import json
from sklearn.linear_model import Ridge
from yellowbrick.regressor import ResidualsPlot
import matplotlib.pyplot as plt
from PIL import Image

def download_model(target_string):
    print("todo")


def does_model_exsit(target_string):
    model_output_loc = "models/rf_reg_" + target_string + "_rf_reg_model.pkl"

    if path.exists(model_output_loc):
        print("model exists")
        return True
    else:
        print("model does not exist")
        return False

@st.cache(allow_output_mutation=True)
def load_model(model_output_loc):
    rf = pickle.load(open(model_output_loc, "rb"))
    return rf


def train_model(rf, healed_data, target_string):
    #rf.fit(healed_data["train_features"], healed_data["train_target"])
    model = Ridge()
    visualizer = ResidualsPlot(rf)
    try:
        visualizer.fit(healed_data["train_features"], healed_data["train_target"])
    except Exception as e:
        st.error("Fit error: "+str(e))
        
    try:
        visualizer.score(healed_data["test_features"],healed_data["test_target"])
    except Exception as e:
        st.error("Score error: "+str(e))
        

    visualizer.show()
    # st.write(visualizer)
    st.pyplot(plt.savefig("models/rf_reg_eval_" + target_string + ".png"))
    # save model output
    model_output_loc = "models/rf_reg_" + target_string + "_rf_reg_model.pkl"
    model_output = open(model_output_loc, "wb")
    pickle.dump(rf, model_output)
    model_output.close()
    print("saving model to: " + model_output_loc)
    return


def eval_model(rf, healed_data):

    train_features = healed_data["train_features"]
    train_target = healed_data["train_target"]
    test_target = healed_data["test_target"]

    test_features = healed_data["test_features"]
    feature_list = healed_data["feature_list"]
    featuresarr = healed_data["features_arr"]
    target = healed_data["target"]
    target_string = healed_data["target_string"]
    raw_data = healed_data["mana"]

    predictions = rf.predict(test_features)
    # print("Predictions:", predictions)
    # print("True Values", test_target)

    errors = abs(predictions - test_target)
    # print("Errors", errors)
    # run_output += 'Errors', errors+"\n"
    # print("The RF Models Mean Absolute Error: ", round(np.mean(errors), 2))
    # run_output += 'The RF Models Mean Absolute Error: ', round(np.mean(errors), 2)+"\n"

    # Calculate mean absolute percentage error (MAPE)
    mape = 100 * (errors / test_target)

    # Calculate and display accuracy
    accuracy = 100 - np.mean(abs(mape))
    # print("Accuracy:", round(accuracy, 2), "%.")
    # run_output += 'Accuracy:', round(accuracy, 2), '%.'+"\n"
    np.set_printoptions(suppress=True)
    # print("MAPE:", mape)
    # run_output += print('MAPE:', mape)+"\n"

    # Get numerical feature importances
    importances = list(rf.feature_importances_)
    importances2 = rf.feature_importances_  # used later for graph
    # List of tuples with variable and importance
    feature_importances = [
        (feature, round(importance, 2))
        for feature, importance in zip(feature_list, importances)
    ]

    # Sort the feature importances by most important first
    feature_importances = sorted(
        feature_importances, key=lambda x: x[1], reverse=True
    )  # print out the feature and importances

    # [
    #     print("Variable: {:20} Importance: {}".format(*pair))
    #     for pair in feature_importances
    # ]

    predictions = rf.predict(featuresarr)
    true = target

    r2 = r2_score(true, predictions)
    mse = mean_squared_error(true, predictions)
    rmse = np.sqrt(mean_squared_error(true, predictions))
    model_output_loc = "models/rf_reg_" + target_string + "_rf_reg_model.pkl"
    # print("R^2 = %.3f" % r2)
    # print("MSE = %.3f" % mse)
    # print("RMSE = %.3f" % rmse)
    jsonOutput = {}
    jsonOutput["model_location"] = model_output_loc
    jsonOutput["r2"] = r2
    jsonOutput["mse"] = mse
    jsonOutput["rmse"] = rmse
    jsonOutput["feature_importances"] = feature_importances
    jsonOutput["predictions"] = predictions.tolist()

    json_path = "models/rf_reg_" + target_string + "_rf_reg_model.json"

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(jsonOutput, f, ensure_ascii=False, indent=4)

    return jsonOutput


def spell(spell_inputs):

    # print("rf_reg heal data")

    # Random hyper parms
    tuned = {}
    tuned["min_samples_leaf"] = 2
    tuned["max_features"] = "sqrt"
    tuned["bootstrap"] = True
    tuned["n_estimators"] = 1000
    tuned["max_depth"] = 150
    tuned["min_samples_split"] = 2

    randInt = random.randint(1, 200)

    rf = RandomForestRegressor(
        n_estimators=tuned["n_estimators"],
        max_features=tuned["max_features"],
        max_depth=tuned["max_depth"],
        min_samples_split=tuned["min_samples_split"],
        bootstrap=tuned["bootstrap"],
        min_samples_leaf=tuned["min_samples_leaf"],
        random_state=randInt,
    )

    # train the model!!!!
    # print("Heres model data")
    healed_data = spell_inputs["healed_data"]

    # print(str(healed_data))
    train_features = healed_data["train_features"]
    train_target = healed_data["train_target"]
    test_target = healed_data["test_target"]

    test_features = healed_data["test_features"]
    feature_list = healed_data["feature_list"]
    featuresarr = healed_data["features_arr"]
    target = healed_data["target"]
    target_string = healed_data["target_string"]
    raw_data = healed_data["mana"]

    # should check if model exists, if it does load model
    jsonOutput = {}
    show_model_eval = None

    st.header("Model Performance")

    if does_model_exsit(target_string):
        model_output_loc = "models/rf_reg_" + target_string + "_rf_reg_model.pkl"
        rf = load_model(model_output_loc)
        json_path = "models/rf_reg_" + target_string + "_rf_reg_model.json"
        show_model_eval = "models/rf_reg_eval_" + target_string + ".png"
        with open(json_path) as json_file:
            jsonOutput = json.load(json_file)
    else:
        try:
            train_model(rf, healed_data, target_string)
        except Exception as e:
            st.error(e)
            st.error("Predictor does not work on string based categories like "+target_string)
            return            
        jsonOutput = eval_model(rf, healed_data)

    if st.checkbox("Show rf_reg raw data"):
        st.write(jsonOutput)

    # show model performance
    
    # st.subheader("r2: " + str(jsonOutput["r2"]))
    # st.subheader("mse: " + str(jsonOutput["mse"]))
    # st.subheader("rmse: " + str(jsonOutput["rmse"]))

    
    feat_df = pd.DataFrame(
        jsonOutput["feature_importances"], columns=["Feature", "Importance"]
    )

    

    # bars = alt.Chart(feat_df).mark_bar().encode(y="Feature", x="Importance")

    # text = bars.mark_text(
    # align='left',
    # baseline='middle',
    # dx=3  # Nudges text to right so it doesn't appear on top of the bar
    # ).encode(
    # text='Feature'
    # )

    # chart = bars+text

    if show_model_eval is not None:
        image = Image.open(show_model_eval)
        st.image(image,caption='Model',use_column_width=True)

    st.header("Feature Importance")
    # st.write(feat_df)

    chart = (
        alt.Chart(feat_df)
        .mark_bar()
        .encode(y=alt.Y('Feature', sort='-x'), x="Importance",tooltip=list(feat_df.columns))
        .properties(title="Feature Importance Chart")
        .configure_title(fontSize=20,)
    ).properties(height=700)
    st.altair_chart(chart, use_container_width=True)

    if st.button("Retrain Model"):
        train_model(rf, healed_data, target_string)
        jsonOutput = eval_model(rf, healed_data)

    # if st.button('Download Model'):
    #     return download_model(target_string)

    st.markdown("### Predict with model")
    predict_feats = {}
    for feat in feature_list:
        predict_feats[feat] = st.number_input("Insert a value for " + feat)

    if len(predict_feats.keys()) == len(feature_list):
        feats_df = pd.DataFrame(predict_feats, index=[0])
        model_predictions = rf.predict(feats_df)
        print("## Predicted " + target_string + ": " + str(model_predictions[0]))
        st.markdown("## Predicted " + target_string + ": " + str(model_predictions[0]))
    
    return rf,raw_data

