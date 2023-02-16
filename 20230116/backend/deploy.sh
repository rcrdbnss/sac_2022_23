#!/bin/bash
cp ../dao.py .
gcloud app deploy api.yaml
rm dao.py
