#!/bin/bash
cp ../dao.py .
gcloud functions deploy [FUNC_NAME] --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/${PROJECT_ID}/databases/(default)/documents/bracelet_reqs/{user}"
rm dao.py
