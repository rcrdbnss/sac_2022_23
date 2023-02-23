gcloud pubsub topics create ${TOPIC}

gcloud pubsub subscriptions create ${PULL_SUBSC_NAME} --topic ${TOPIC}
