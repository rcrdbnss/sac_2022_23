#!/bin/bash
cp ../dao.py .
gcloud functions deploy update_bills --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/${PROJECT_ID}/databases/(default)/documents/readings/{date}"
rm dao.py
