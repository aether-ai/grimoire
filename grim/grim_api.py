from flask import Flask
from flask import request
from flask_cors import CORS
import os
import json
import pandas as pd
import sys, logging
from spells import REGISTERED_SPELLS
from flask import jsonify
import glob

logLevel = logging.DEBUG
logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s | %(levelname)s : %(message)s",
    level=logLevel,
    stream=sys.stdout,
)
logger.warning("Log Level set to: {}".format(logLevel))
application = Flask(__name__)
CORS(application)


@application.route("/health")
def health():
    jsonResp = {}
    jsonResp["healthy"] = "true"
    return jsonify(jsonResp)


@application.route("/reset_grim", methods=["GET", "POST"])
def reset_test():
    """
    Purpose:
        reset test grim
    Args/Requests:
         data = metadata needed to create grim 
    Return:
        json object with result of reset
    """
    jsonResp = {}
    try:
        cmd = "cp test_grims/test_run_clean.json grim_st.json"
        os.system(cmd)
        cmd = "cp test_grims/test_run_clean.json test_grims/test_run.json"
        os.system(cmd)
        jsonResp["status"] = "test reset"
    except Exception as e:
        logging.info("Yikes bad error")
        logging.error(e)
        jsonResp["error"] = "Segfault..." + str(e)
        return jsonify(jsonResp)
    return jsonify(jsonResp)


@application.route("/launch_test_grim", methods=["GET", "POST"])
def launch_test_grim():
    """
    Purpose:
        Launch grimoire
    Args/Requests:
         data = metadata needed to launch grim
    Return:
        json object with status of launch
    """
    data = request.data
    # hmm have streamlit run from start, and then have it just refresh
    # instead of spawning new prorcces
    grimoire = json.loads(data.decode("utf-8"))
    grimoire["isTest"] = True
    # print(grimoire["name"])
    # run streamlit spell runner
    # basicaly we want to refresh grim_st with the grim path
    # we are just going to dump grim to grim_st.json
    with open("grim_st.json", "w") as outfile:
        json.dump(grimoire, outfile)
    # cmd = "streamlit run grim_st.py "+grimoire["spell_path"]+" &"
    # os.system(cmd)
    jsonResp = {}
    jsonResp["status"] = "good"
    return jsonify(jsonResp)


@application.route("/test_grim", methods=["GET", "POST"])
def test_grim():
    """
    Purpose:
        test grim
    Args/Requests:
         data = metadata needed to test grim 
    Return:
        json object with result of test
    """
    jsonResp = {}
    data = request.data
    try:
        spells = json.loads(data.decode("utf-8"))
        spells_to_add = spells["spells"]
        grim_path = "test_grims/test_run.json"
        with open(grim_path) as json_file:
            grimoire = json.load(json_file)

        # clear spells, then add
        grimoire["spells"] = []
        grimoire["spells"].extend(spells_to_add)

        # write the json to cast path dont have to save it, but will allow for now
        with open(grim_path, "w") as outfile:
            json.dump(grimoire, outfile)

        # need to trigger update for streamlit here
        cmd = "cp test_grims/test_run.json grim_st.json"
        os.system(cmd)
        # I hate it too, but no other way to auto update streamlit
        lines = []
        with open("grim_st.py") as infile:
            for line in infile:
                if "###### Grimoire Streamlit Runner ######" in line:
                    # print("found replace")
                    line = line.replace(
                        "###### Grimoire Streamlit Runner ######",
                        "##### Grimoire Streamlit Runner #####",
                    )
                elif "##### Grimoire Streamlit Runner #####" in line:
                    # print("found replace")
                    line = line.replace(
                        "##### Grimoire Streamlit Runner #####",
                        "###### Grimoire Streamlit Runner ######",
                    )
                lines.append(line)
        with open("grim_st.py", "w") as outfile:
            for line in lines:
                outfile.write(line)

    except Exception as e:
        logging.info("Yikes bad error")
        logging.error(e)
        jsonResp["error"] = "Segfault..." + str(e)
        return jsonify(jsonResp)

    jsonResp["status"] = "got it"
    jsonResp["grim_path"] = grim_path
    return jsonify(jsonResp)


@application.route("/create_grim", methods=["GET", "POST"])
def create_grim():
    """
    Purpose:
        Create grim
    Args/Requests:
         data = metadata needed to create grim 
    Return:
        json object with result of create
    """
    jsonResp = {}
    data = request.data
    try:
        grimoire = json.loads(data.decode("utf-8"))
        grim_path = "grimoire/" + grimoire["name"] + ".json"
        grimoire["spell_path"] = grim_path
        # check if grim exists
        if os.path.exists(grim_path):
            jsonResp["error"] = "Grimoire already exists"
            return jsonify(jsonResp)
        # write the json to cast path
        with open(grim_path, "w") as outfile:
            json.dump(grimoire, outfile)

    except Exception as e:
        logging.info("Yikes bad error")
        logging.error(e)
        jsonResp["error"] = "Segfault..." + str(e)
        return jsonify(jsonResp)

    jsonResp["status"] = "got it"
    jsonResp["grim_path"] = grim_path
    return jsonify(jsonResp)


@application.route("/launch_grim", methods=["GET", "POST"])
def launch_grim():
    """
    Purpose:
        Launch grimoire
    Args/Requests:
         data = metadata needed to launch grim 
    Return:
        json object with result of launch
    """
    data = request.data
    # hmm have streamlit run from start, and then have it just refresh
    # instead of spawning new prorcces
    grimoire = json.loads(data.decode("utf-8"))
    # run streamlit spell runner
    # basicaly we want to refresh grim_st with the grim path
    # we are just going to dump grim to grim_st.json
    with open("grim_st.json", "w") as outfile:
        json.dump(grimoire, outfile)
    jsonResp = {}
    jsonResp["status"] = "good"
    return jsonify(jsonResp)



@application.route("/download_grim", methods=["GET", "POST"])
def download_grim():
    """
    Purpose:
        Download grimoire
    Args/Requests:
         data = metadata needed to download grim 
    Return:
        json object with result of download
    """
    data = request.data
    # hmm have streamlit run from start, and then have it just refresh
    # instead of spawning new prorcces
    grim = json.loads(data.decode("utf-8"))

    #zip up files and send to nginx downloads folder
    #provide link, hmm hardcode local host for now? will have to update to host ip...

    #make temp dir
    os.system("mkdir -p temp_grim/spells/")

    #copy grim_st.py
    os.system("cp grim_st.py temp_grim/")
    os.system("cp grim_st.json temp_grim/")

    #copy spell init
    os.system("cp spells/__init__.py temp_grim/spells/")

    #copy assets
    os.system("cp -r assets temp_grim/")

    #copy spells
    for spell in grim["spells"]:
        spell_name = spell["spell_name"]
        spell_type = spell["spell_type"]

        #make spell dir
        cmd = "mkdir -p temp_grim/spells/"+spell_type+"/"
        os.system(cmd)

        #copy spell json and py
        cmd = "cp spells/"+spell_type+"/"+spell_name+".* temp_grim/spells/"+spell_type+"/"
        os.system(cmd)

    grim_name = grim["name"].replace(" ","_")+"_grimoire.zip"

    # Do the zip here too...
    cmd = "zip "+grim_name+" -r temp_grim"
    os.system(cmd)
    # move to zip dir
    cmd = "mv "+grim_name+" /var/www/html/zips/"
    os.system(cmd)

    #remove temp grim
    cmd = "rm -rf temp_grim/"
    os.system(cmd)


    jsonResp = {}
    jsonResp["status"] = "good"
    jsonResp["url"] = "/zips/"+grim_name
    return jsonify(jsonResp)



@application.route("/get_grims")
def get_grims():
    """
    Purpose:
        Get grimoire json files
    Args/Requests:
         N/A
    Return:
        array of grim objects
    """
    grim_array = []
    jsonResp = {}
    # local grim file
    for file in os.listdir("grimoire"):
        if file.endswith(".json"):
            try:
                # logging.info(os.path.join("grimoire", file))
                with open(os.path.join("grimoire", file)) as json_file:
                    grim = json.load(json_file)
                    # logging.info(grim)
                    grim_array.append(grim)

            except Exception as e:
                logging.info("Yikes bad error")
                logging.error(e)
                jsonResp["error"] = "Segfault..." + str(e)
                return jsonResp
    jsonResp["grims"] = grim_array

    return jsonify(jsonResp)


def spell_display_name(spell):

    if spell == "holy":
        return "Data Cleaning (Holy)"
    elif spell == "nature":
        return "Data Visualization (Nature)"
    elif spell == "arcane":
        return "Machine Learning (Arcane)"
    elif spell == "water":
        return "Data Query (Water)"
    elif spell == "air":
        return "Map Visualization (Air)"
    elif spell == "time":
        return "Data Animation (Time)"
    else:
        return "Custom (User Defined)"


@application.route("/get_spells")
def get_spells():
    """
    Purpose:
        Get spell json files
    Args/Requests:
         N/A
    Return:
        array of spell objects
    """
    spells_array = []
    jsonResp = {}
    try:
        file_list = glob.glob("spells/**/*.json")
        for spell_json in file_list:
            with open(spell_json) as json_file:
                spell_data = json.load(json_file)
                if "spell_image" not in spell_data:
                    possible_path = (
                        "../../assets/spell_images/"
                        + spell_data["spell_type"]
                        + "/"
                        + spell_data["spell_name"]
                        + ".png"
                    )
                    spell_data["spell_image"] = possible_path
                spells_array.append(spell_data)
    except Exception as e:
        logging.info("Yikes bad error")
        logging.error(e)
        jsonResp["error"] = "Segfault..." + str(e)
        return jsonResp
    spells_map = {}

    for spell in spells_array:
        spell_key = spell_display_name(spell["spell_type"])
        if spell_key not in spells_map:
            spells_map[spell_key] = []
            spells_map[spell_key].append(spell)
        else:
            spells_map[spell_key].append(spell)
    jsonResp["spells"] = spells_array
    jsonResp["spells_map"] = spells_map
    return jsonify(jsonResp)


if __name__ == "__main__":
    loglevel = logging.INFO
    logging.basicConfig(format="%(levelname)s: %(message)s", level=loglevel)
    application.run(host="0.0.0.0", port="9000")
