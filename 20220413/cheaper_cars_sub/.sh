export PROJECT_ID=rbenassi-20220413

export TOPIC=cheaper_cars

export PULL_SUBSC_NAME=cheaper_cars_pull_sub

export PUSH_SUBSC_NAME=cheaper_cars_push_sub

export TOKEN=zxcvtoken

gcloud pubsub subscriptions create ${PULL_SUBSC_NAME} --topic ${TOPIC}

gcloud pubsub topics publish ${TOPIC} --attribute=from="cli" --message="Test message"

gcloud pubsub subscriptions create ${PUSH_SUBSC_NAME} --topic ${TOPIC} --push-endpoint \
"https://${PROJECT_ID}.appspot.com/pubsub/push?token=${TOKEN}" --ack-deadline=10
