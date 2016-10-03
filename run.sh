#!/bin/bash
cd hackernews

virtualenv .venv
source ./.venv/bin/activate
pip install -r requirements.txt

cd hackernewsclone
python hackernews.py