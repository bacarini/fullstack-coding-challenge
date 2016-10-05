#!/bin/bash

CONFIGPATH=~/.unbabel

function configure_unbabel(){
    echo "Please, enter your Unbabel api username"
    read api_username
    echo "Please, enter your Unbabel api key"
    read api_key
    echo "[Sandbox]" > "$CONFIGPATH"
    echo "UNBABEL_API_USERNAME=$api_username" >> "$CONFIGPATH"
    echo "UNBABEL_API_KEY=$api_key" >> "$CONFIGPATH"
    echo "Nice! Now you already to go ahead with Unbabel API!"
}


function run_app(){
    cd hackernews
    virtualenv .venv
    source ./.venv/bin/activate
    pip install -r requirements.txt
    cd hackernewsclone
    python hackernews.py
}


if [ -f "$CONFIGPATH" ]
then
    echo "Unbabel credential is already configured. $CONFIGPATH found."
    echo "Let's go install and run The App."
    run_app;
else
    echo "We do not founded your Unbabel credentials in $CONFIGPATH path"
    while true; do
        read -p "Let's go configure your Unbabel credentials (yes/no)?" yn
        case $yn in
            [Yy]* ) configure_unbabel; break;;
            [Nn]* ) break;;
            * ) echo "Please enter only yes or no.";;
        esac
    done
fi

