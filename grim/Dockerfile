FROM python:3.6.8

# Copy dependency definitions
ADD docker_environment /tmp/docker_environment

# Install Python Dependencies
RUN pip install -r /tmp/docker_environment/python_packages.txt

# Install Linux Dependencies 
RUN apt-get update; apt-get install -y $(awk '{print $1'} /tmp/docker_environment/linux_packages.txt)
RUN bash /tmp/docker_environment/custom.sh

# Copy Grimoire Files
COPY grim*.py /home/
COPY startup.sh /home/
ADD spells /home/spells
ADD helpers /home/helpers
ADD .streamlit /home/.streamlit 
ADD sample_data /home/sample_data
ADD test_grims /home/test_grims
ADD test_grims/test_run_clean.json  /home/grim_st.json
ADD grim_ui/html /var/www/html
ADD sample_grims /home/grimoire
ADD assets /home/assets

EXPOSE 8501 9000 9005

WORKDIR /home/

CMD ["bash", "./startup.sh"]
