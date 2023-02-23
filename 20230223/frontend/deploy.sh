#!/bin/bash
cp ../dao.py .
cp ../common.py .
gcloud app deploy
rm dao.py
rm common.py
