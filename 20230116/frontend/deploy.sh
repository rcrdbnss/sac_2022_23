#!/bin/bash
cp ../dao.py .
gcloud app deploy
rm dao.py
