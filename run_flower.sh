#!/bin/bash

function run_celery(){
    cd hackernews
    virtualenv .venv
    source ./.venv/bin/activate
    pip install -r requirements.txt
    cd hackernewsclone
    flower -A tasks --port=5555 --broker=redis://
}

run_celery;

