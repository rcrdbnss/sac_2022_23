export PROJECT_ID=rbenassi-20220224

gcloud functions deploy hand_irrigator --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/${PROJECT_ID}/databases/(default)/documents/hand_irr/{timestamp}"

gcloud functions deploy humidity_update --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/${PROJECT_ID}/databases/(default)/documents/humidity/{timestamp}"
