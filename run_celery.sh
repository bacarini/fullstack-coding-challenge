#!/bin/bash

function run_celery(){
    cd hackernews
    virtualenv .venv
    source ./.venv/bin/activate
    pip install -r requirements.txt
    cd hackernewsclone
    celery -A tasks worker -B --loglevel=info
}

run_celery;

