export PROJECT_ID=rbenassi-20220413

export TOPIC=cheaper_cars

gcloud functions deploy check_prices --runtime=python39 --trigger-event="providers/cloud.firestore/eventTypes/document.write" --trigger-resource="projects/${PROJECT_ID}/databases/(default)/documents/users/{email}"

gcloud pubsub topics create ${TOPIC}
