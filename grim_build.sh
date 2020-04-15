#!/bin/bash
echo "Building Grimoire UI"
#build ionic app
cd grim/grim_ui/
ionic build --prod
cd ../
#Build docker image
echo "Building Grimoire Docker Image"
docker build $@ -t aetheraidocker/grimoire:demo_site .
cd ../
echo "Build Complete"
