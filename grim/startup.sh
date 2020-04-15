#!/bin/bash

#start nginx
service nginx start

#start backend api
gunicorn --bind 0.0.0.0:9000 --timeout 600 --workers=2 --reload grim_api &
#start streamlit server
streamlit run grim_st.py &

#stay up forever
tail -f /dev/null
