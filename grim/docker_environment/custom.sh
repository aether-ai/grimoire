#!/bin/bash

#make data dirs
mkdir -p /home/spells
mkdir -p /home/helpers
mkdir -p /home/models
mkdir -p /home/models/fasttext
mkdir -p /home/data_files
mkdir -p /home/data_files/audio
mkdir -p /home/data_files/images
mkdir -p /home/data_files/text
mkdir -p /var/www/html/zips

#replace 404 in nginx
sed -i 's/=404/\/index.html/g' /etc/nginx/sites-available/default

#download spacy models
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_md
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_core_sci_sm-0.2.4.tar.gz